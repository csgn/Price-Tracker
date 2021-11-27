import React, { useState } from 'react';
import {
  Alert,
  Button,
  Form,
  FormControl,
  FormGroup,
  FormLabel,
  Spinner,
} from 'react-bootstrap';

import axios from 'axios';

export default function TrackPage() {
  const [error, setError] = useState();
  const [loading, setLoading] = useState();
  const [message, setMessage] = useState();

  const handleSubmit = (event) => {
    event.preventDefault();

    const data = event.target[0].value;
    const urls = data.split('\n').filter((el) => {
      return el !== '';
    });

    if (urls.length === 0) {
      setError('Please enter a url');
      return;
    }

    setLoading(true);
    setMessage(null);
    setError(null);

    axios
      .post(
        'http://localhost:4444/track',
        {
          urls,
        },
        {
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
          },
        }
      )
      .then((res) => {
        setError(null);
        setLoading(false);
        setMessage('Product(s) is being tracked');
      })
      .catch((err) => {
        console.error(err);
        setError('Something went wrong');
      });
  };

  return (
    <div className="m-5">
      <Form onSubmit={handleSubmit}>
        <FormLabel>Enter URLs</FormLabel>
        <FormGroup>
          <FormControl
            as="textarea"
            rows={10}
            id="urlTextAreaHelp"
            size="sm"
          ></FormControl>
          <small id="urlTextAreaHelp" className="form-text text-muted">
            Press enter if you want tracking many url
          </small>
        </FormGroup>
        <FormGroup>
          <Button
            type="submit"
            className="mt-3"
            disabled={loading ? true : false}
          >
            <span className="p-2">Add Into Tracking List</span>
            {loading && (
              <Spinner animation="border" role="status" size="sm"></Spinner>
            )}
          </Button>
        </FormGroup>
      </Form>
      {message ? (
        <Alert variant="success" className="mt-2">
          {message}
        </Alert>
      ) : (
        error && (
          <Alert variant="danger" className="mt-2">
            {error}
          </Alert>
        )
      )}
    </div>
  );
}
