const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const number = new Intl.NumberFormat("en-US");

const state = {
  data: null,
  store: "all",
  category: "all",
};

const elements = {
  loadingState: document.querySelector("#loadingState"),
  errorState: document.querySelector("#errorState"),
  dashboardContent: document.querySelector("#dashboardContent"),
  storeFilter: document.querySelector("#storeFilter"),
  categoryFilter: document.querySelector("#categoryFilter"),
  resetFilters: document.querySelector("#resetFilters"),
  totalSales: document.querySelector("#totalSales"),
  transactions: document.querySelector("#transactions"),
  itemsSold: document.querySelector("#itemsSold"),
  averageOrder: document.querySelector("#averageOrder"),
  dateRange: document.querySelector("#dateRange"),
  lineChart: document.querySelector("#lineChart"),
  categoryBars: document.querySelector("#categoryBars"),
  storeBars: document.querySelector("#storeBars"),
  productList: document.querySelector("#productList"),
  sampleRows: document.querySelector("#sampleRows"),
};

function showContent() {
  elements.loadingState.classList.add("hidden");
  elements.errorState.classList.add("hidden");
  elements.dashboardContent.classList.remove("hidden");
}

function showError() {
  elements.loadingState.classList.add("hidden");
  elements.dashboardContent.classList.add("hidden");
  elements.errorState.classList.remove("hidden");
}

function filterBySelection(rows, key, selected) {
  if (selected === "all") {
    return rows;
  }

  return rows.filter((row) => row[key] === selected);
}

function getFilteredData() {
  const data = structuredClone(state.data);

  data.category = filterBySelection(data.category, "category", state.category);
  data.store = filterBySelection(data.store, "store", state.store);
  data.topProducts = filterBySelection(data.topProducts, "productCategory", state.category);
  data.sampleRows = data.sampleRows.filter((row) => {
    const storeMatches = state.store === "all" || row.storeLocation === state.store;
    const categoryMatches = state.category === "all" || row.productCategory === state.category;
    return storeMatches && categoryMatches;
  });

  const categoryScale = new Set(data.category.map((item) => item.category));
  const storeScale = new Set(data.store.map((item) => item.store));
  data.daily = data.daily.map((day) => {
    const sampleRatio =
      (state.category === "all" ? 1 : Math.max(categoryScale.size, 1) / state.data.filters.categories.length) *
      (state.store === "all" ? 1 : Math.max(storeScale.size, 1) / state.data.filters.stores.length);

    return {
      ...day,
      totalSales: day.totalSales * sampleRatio,
      transactions: Math.round(day.transactions * sampleRatio),
      itemsSold: Math.round(day.itemsSold * sampleRatio),
    };
  });

  const totals = [...data.category, ...data.store].reduce(
    (acc, row) => {
      acc.totalSales += row.totalSales;
      acc.itemsSold += row.itemsSold;
      acc.transactions += row.transactions;
      return acc;
    },
    { totalSales: 0, itemsSold: 0, transactions: 0 },
  );

  if (state.category === "all" && state.store === "all") {
    data.totals = state.data.totals;
  } else {
    data.totals = {
      totalSales: totals.totalSales / (state.category !== "all" && state.store !== "all" ? 2 : 1),
      itemsSold: Math.round(totals.itemsSold / (state.category !== "all" && state.store !== "all" ? 2 : 1)),
      transactions: Math.round(totals.transactions / (state.category !== "all" && state.store !== "all" ? 2 : 1)),
    };
    data.totals.averageOrder = data.totals.transactions
      ? data.totals.totalSales / data.totals.transactions
      : 0;
  }

  return data;
}

function populateFilters(data) {
  for (const store of data.filters.stores) {
    elements.storeFilter.insertAdjacentHTML("beforeend", `<option value="${store}">${store}</option>`);
  }

  for (const category of data.filters.categories) {
    elements.categoryFilter.insertAdjacentHTML("beforeend", `<option value="${category}">${category}</option>`);
  }
}

function updateMetrics(data) {
  elements.totalSales.textContent = money.format(data.totals.totalSales);
  elements.transactions.textContent = number.format(data.totals.transactions);
  elements.itemsSold.textContent = number.format(data.totals.itemsSold);
  elements.averageOrder.textContent = money.format(data.totals.averageOrder);
}

function renderLineChart(rows) {
  const width = 920;
  const height = 330;
  const pad = 24;
  const max = Math.max(...rows.map((row) => row.totalSales));
  const min = Math.min(...rows.map((row) => row.totalSales));
  const spread = max - min || 1;

  const points = rows.map((row, index) => {
    const x = pad + (index / Math.max(rows.length - 1, 1)) * (width - pad * 2);
    const y = height - pad - ((row.totalSales - min) / spread) * (height - pad * 2);
    return { x, y, row };
  });

  const line = points.map((point) => `${point.x},${point.y}`).join(" ");
  const area = `${pad},${height - pad} ${line} ${width - pad},${height - pad}`;
  const dots = points
    .filter((_, index) => index % 10 === 0 || index === points.length - 1)
    .map(
      (point) =>
        `<circle class="chart-dot" cx="${point.x}" cy="${point.y}" r="4"><title>${point.row.date}: ${money.format(
          point.row.totalSales,
        )}</title></circle>`,
    )
    .join("");

  elements.dateRange.textContent = `${rows[0].date} to ${rows.at(-1).date}`;
  elements.lineChart.innerHTML = `
    <svg class="chart-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
      <polyline class="chart-area" points="${area}"></polyline>
      <polyline class="chart-line" points="${line}"></polyline>
      ${dots}
    </svg>
  `;
}

function renderBars(container, rows, labelKey, limit = 8) {
  const selectedRows = rows.slice(0, limit);
  const max = Math.max(...selectedRows.map((row) => row.totalSales), 1);
  container.innerHTML = selectedRows
    .map((row) => {
      const width = Math.max((row.totalSales / max) * 100, 3);
      return `
        <div class="bar-row">
          <div class="bar-meta">
            <span>${row[labelKey]}</span>
            <span>${money.format(row.totalSales)}</span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width: ${width}%"></div></div>
        </div>
      `;
    })
    .join("");
}

function renderProducts(rows) {
  elements.productList.innerHTML = rows
    .slice(0, 10)
    .map(
      (row, index) => `
        <div class="product-item">
          <span class="rank">${String(index + 1).padStart(2, "0")}</span>
          <div>
            <div class="product-name">${row.productDetail}</div>
            <div class="product-category">${row.productCategory}</div>
          </div>
          <strong class="product-value">${money.format(row.totalSales)}</strong>
        </div>
      `,
    )
    .join("");
}

function renderTable(rows) {
  elements.sampleRows.innerHTML = rows
    .slice(0, 80)
    .map(
      (row) => `
        <tr>
          <td>${row.transactionId}</td>
          <td>${row.transactionDate}</td>
          <td>${row.storeLocation}</td>
          <td>${row.productCategory}</td>
          <td>${row.productDetail}</td>
          <td>${money.format(row.totalAmount)}</td>
        </tr>
      `,
    )
    .join("");
}

function render() {
  const data = getFilteredData();
  updateMetrics(data);
  renderLineChart(data.daily);
  renderBars(elements.categoryBars, data.category, "category");
  renderBars(elements.storeBars, data.store, "store");
  renderProducts(data.topProducts);
  renderTable(data.sampleRows);
  showContent();
}

async function init() {
  try {
    const response = await fetch("./data.json");
    state.data = await response.json();
    populateFilters(state.data);
    render();
  } catch {
    showError();
  }
}

elements.storeFilter.addEventListener("change", (event) => {
  state.store = event.target.value;
  render();
});

elements.categoryFilter.addEventListener("change", (event) => {
  state.category = event.target.value;
  render();
});

elements.resetFilters.addEventListener("click", () => {
  state.store = "all";
  state.category = "all";
  elements.storeFilter.value = "all";
  elements.categoryFilter.value = "all";
  render();
});

init();
