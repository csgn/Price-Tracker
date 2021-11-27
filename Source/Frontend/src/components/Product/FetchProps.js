import axios from 'axios';

const ORIGIN = 'http://localhost:8000/products';

export async function fetchProductBrand(productid, callback) {
  await axios
    .get(`${ORIGIN}/${productid}/brand/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProductSubcategory(productid, callback) {
  await axios
    .get(`${ORIGIN}/${productid}/subcategory/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProductCategory(productid, callback) {
  await axios
    .get(`${ORIGIN}/${productid}/category/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProductSupplier(productid, callback) {
  await axios.get(`${ORIGIN}/${productid}/supplier/`).then(async (res) => {
    callback(res.data);
  });
}

export async function fetchProductPrice(productid, callback) {
  await axios
    .get(`${ORIGIN}/${productid}/price/`)
    .then(async (res) => {
      let data = res.data;
      data.map((el) => {
        el.startdate = new Date(el.startdate)
          .toISOString()
          .split('T')[0]
          .toString();
      });

      callback(data);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProduct(productid, callback) {
  await axios
    .get(`${ORIGIN}/${productid}/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export async function fetchProducts(callback) {
  await axios
    .get(`${ORIGIN}/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}
