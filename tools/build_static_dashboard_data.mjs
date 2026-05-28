import { mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = dirname(dirname(fileURLToPath(import.meta.url)));
const sourceDir = join(rootDir, "online_dashboard");
const distDir = join(rootDir, "dist");
const cleanCsvPath = join(rootDir, "data", "processed", "clean_sales.csv");
const dashboardDataPath = join(sourceDir, "data.json");

function parseCsv(text) {
  const rows = [];
  let field = "";
  let row = [];
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (char === '"' && quoted && next === '"') {
      field += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(field);
      field = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") {
        index += 1;
      }
      row.push(field);
      if (row.some((value) => value.length > 0)) {
        rows.push(row);
      }
      row = [];
      field = "";
    } else {
      field += char;
    }
  }

  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  const [headers, ...records] = rows;
  return records.map((record) =>
    Object.fromEntries(headers.map((header, index) => [header, record[index] ?? ""])),
  );
}

function roundMoney(value) {
  return Math.round((value + Number.EPSILON) * 100) / 100;
}

function addGroup(map, key, amount, quantity, transactionId) {
  const current = map.get(key) ?? {
    key,
    totalSales: 0,
    itemsSold: 0,
    transactions: 0,
    transactionIds: new Set(),
  };

  current.totalSales += amount;
  current.itemsSold += quantity;
  current.transactionIds.add(transactionId);
  current.transactions = current.transactionIds.size;
  map.set(key, current);
}

function serializeGroup(item, keyName) {
  return {
    [keyName]: item.key,
    totalSales: roundMoney(item.totalSales),
    itemsSold: item.itemsSold,
    transactions: item.transactions,
  };
}

async function regenerateDataJson() {
  let csvText;
  try {
    csvText = await readFile(cleanCsvPath, "utf8");
  } catch {
    return;
  }

  const rows = parseCsv(csvText);
  const daily = new Map();
  const category = new Map();
  const store = new Map();
  const product = new Map();
  let totalSales = 0;
  let totalItems = 0;
  const transactionIds = new Set();
  const categories = new Set();
  const stores = new Set();

  for (const row of rows) {
    const amount = Number(row.total_amount);
    const quantity = Number(row.transaction_qty);
    const transactionId = row.transaction_id;
    const date = row.transaction_date;
    const categoryName = row.product_category;
    const storeName = row.store_location;
    const productKey = `${row.product_detail}|||${row.product_category}`;

    totalSales += amount;
    totalItems += quantity;
    transactionIds.add(transactionId);
    categories.add(categoryName);
    stores.add(storeName);

    addGroup(daily, date, amount, quantity, transactionId);
    addGroup(category, categoryName, amount, quantity, transactionId);
    addGroup(store, storeName, amount, quantity, transactionId);
    addGroup(product, productKey, amount, quantity, transactionId);
  }

  const productRows = [...product.values()]
    .map((item) => {
      const [productDetail, productCategory] = item.key.split("|||");
      return {
        productDetail,
        productCategory,
        totalSales: roundMoney(item.totalSales),
        itemsSold: item.itemsSold,
        transactions: item.transactions,
      };
    })
    .sort((a, b) => b.totalSales - a.totalSales)
    .slice(0, 20);

  const sampleRows = rows.slice(-200).reverse().map((row) => ({
    transactionId: Number(row.transaction_id),
    transactionDate: row.transaction_date,
    storeLocation: row.store_location,
    productCategory: row.product_category,
    productDetail: row.product_detail,
    quantity: Number(row.transaction_qty),
    unitPrice: Number(row.unit_price),
    totalAmount: Number(row.total_amount),
  }));

  const payload = {
    generatedAt: new Date().toISOString(),
    source: "Brewline Sales Analytics ETL output",
    totals: {
      totalSales: roundMoney(totalSales),
      transactions: transactionIds.size,
      itemsSold: totalItems,
      averageOrder: roundMoney(totalSales / transactionIds.size),
      categories: categories.size,
      stores: stores.size,
    },
    filters: {
      categories: [...categories].sort(),
      stores: [...stores].sort(),
    },
    daily: [...daily.values()]
      .map((item) => serializeGroup(item, "date"))
      .sort((a, b) => a.date.localeCompare(b.date)),
    category: [...category.values()]
      .map((item) => serializeGroup(item, "category"))
      .sort((a, b) => b.totalSales - a.totalSales),
    store: [...store.values()]
      .map((item) => serializeGroup(item, "store"))
      .sort((a, b) => b.totalSales - a.totalSales),
    topProducts: productRows,
    sampleRows,
  };

  await writeFile(dashboardDataPath, `${JSON.stringify(payload, null, 2)}\n`);
}

async function copyStaticFiles() {
  await rm(distDir, { recursive: true, force: true });
  await mkdir(distDir, { recursive: true });

  const files = await readdir(sourceDir);
  await Promise.all(
    files.map(async (file) => {
      const content = await readFile(join(sourceDir, file));
      await writeFile(join(distDir, file), content);
    }),
  );
}

await regenerateDataJson();
await copyStaticFiles();
