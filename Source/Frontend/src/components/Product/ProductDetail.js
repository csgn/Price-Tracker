import React, { useEffect, useState } from 'react';
import { Accordion, Badge, Table, Breadcrumb, Row, Col } from 'react-bootstrap';
import ProductChart from './ProductChart';
import ProductCarousel from './ProductCarousel';

export default function ProductDetail(props) {
  const [loading, setLoading] = useState(true);
  const { product, price, supplier, brand, category, subcategory } = props;

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) return <div>Loading...</div>;

  const suppliersOfPrice = supplier.map((el) => {
    return {
      ...el,
      price: price.filter((pel) => {
        return pel.supplierid === el.supplierid;
      }),
    };
  });

  const sortedSuppliersOfPrice = suppliersOfPrice.sort((a, b) => {
    if (a.price[0].amount < b.price[0].amount) return -1;
    return a.price[0].amount > b.price[0].amount ? 1 : 0;
  });

  const currentSupplier = sortedSuppliersOfPrice[0];
  const currentPrice = sortedSuppliersOfPrice[0].price;

  return (
    <>
      <Row>
        <Col>
          <Breadcrumb>
            <Breadcrumb.Item href={category.url}>
              {category.name}
            </Breadcrumb.Item>
            {subcategory.map((el) => {
              return <Breadcrumb.Item href={el.url}>{el.name}</Breadcrumb.Item>;
            })}
          </Breadcrumb>
        </Col>
      </Row>

      <Row>
        <Col xs={8} md={4}>
          <ProductCarousel images={product?.images} />
        </Col>
        <Col xs={8} md={8}>
          <div className="h5">{product?.name}</div>
          <a href={brand.url} className="text-decoration-none">
            {brand.name}
          </a>
          <div className="mt-3">
            <span className="h2">
              <b>{currentPrice[0].amount}</b>
            </span>
            <i>TL</i>
          </div>
          <div>
            Supplier :
            <a className="m-2 text-decoration-none" href={currentSupplier.url}>
              {currentSupplier.name}
            </a>
          </div>
        </Col>
      </Row>
      <Row>
        <Col>
          <ProductChart supplier={currentSupplier} price={currentPrice} />
        </Col>
      </Row>
      <Row>
        <Col>
          <Accordion defaultActiveKey="0">
            <Accordion.Item eventKey="">
              <Accordion.Header>Another Suppliers</Accordion.Header>
              <Accordion.Body>
                <Table striped bordered hover size="sm">
                  <tbody>
                    {sortedSuppliersOfPrice.map((el) => {
                      return (
                        <tr key={el.supplierid}>
                          <td>
                            <a
                              className="h6 text-decoration-none"
                              href={el.url}
                            >
                              {el.name}
                            </a>
                            <Badge
                              bg={el.rate < 5.0 ? 'danger' : 'success'}
                              className="m-2"
                            >
                              {el.rate}
                            </Badge>
                          </td>
                          <td>
                            <span className="h5">{el.price[0].amount}</span>
                            <i className="m-1">TL</i>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </Table>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </Col>
      </Row>
    </>
  );
}
