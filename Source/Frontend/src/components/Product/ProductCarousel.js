import React from 'react';
import { Carousel, CarouselItem, CardImg } from 'react-bootstrap';

export default function ProductCarousel(props) {
  return (
    <Carousel variant="dark">
      {props.images !== undefined &&
        props.images.map((img) => {
          return (
            <CarouselItem key={img}>
              <CardImg src={img}></CardImg>
            </CarouselItem>
          );
        })}
    </Carousel>
  );
}
