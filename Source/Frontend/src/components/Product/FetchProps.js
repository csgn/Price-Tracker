import axios from 'axios';

const ORIGIN = 'http://localhost:8000/products';

export function fetchProductBrand(productid, callback) {
  axios
    .get(`${ORIGIN}/${productid}/brand/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export function fetchProductSubcategory(productid, callback) {
  axios
    .get(`${ORIGIN}/${productid}/subcategory/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}

export function fetchProductCategory(productid, callback) {
  axios
    .get(`${ORIGIN}/${productid}/category/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export function fetchProductSupplier(productid, callback) {
  axios.get(`${ORIGIN}/${productid}/supplier/`).then(async (res) => {
    callback(res.data);
  });
}

export function fetchProductPrice(productid, callback) {
  axios
    .get(`${ORIGIN}/${productid}/price/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}

export function fetchProduct(productid, callback) {
  axios
    .get(`${ORIGIN}/${productid}/`)
    .then(async (res) => {
      callback(res.data[0]);
    })
    .catch((err) => {
      console.error(err);
    });
}

export function fetchProducts(callback) {
  axios
    .get(`${ORIGIN}/`)
    .then(async (res) => {
      callback(res.data);
    })
    .catch((err) => {
      console.error(err);
    });
}
