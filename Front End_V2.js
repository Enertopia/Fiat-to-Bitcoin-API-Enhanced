import React, { useState } from 'react';
import { Button, Form, Spinner, Alert, Row, Col } from 'react-bootstrap';
import axios from 'axios';

const ConversionForm = ({ onPreview }) => {
    const [amount, setAmount] = useState(0);
    const [percentage, setPercentage] = useState(5);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handlePreview = async (e) => {
        e.preventDefault();
        if(amount <= 0) {
            setError("Please enter a valid amount greater than zero.");
            return;
        }
        setIsLoading(true);
        setError('');

        try {
            const response = await axios.post('https://yourserver.com/preview_convert', {
                amount_fiat: amount,
                conversion_percentage: percentage / 100,
            });
            onPreview(response.data);
        } catch (err) {
            const message = err.response?.data?.message || "Failed to preview conversion. Please try again.";
            setError(message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Form onSubmit={handlePreview}>
            <Row>
                <Col>
                    <Form.Group controlId="amountFiat">
                        <Form.Label>Amount in Fiat</Form.Label>
                        <Form.Control
                            type="number"
                            value={amount}
                            onChange={e => setAmount(parseFloat(e.target.value))}
                            placeholder="Enter total amount in fiat"
                            min="1" // minimum value set to 1 to avoid non-positive numbers
                            required
                        />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group controlId="conversionPercentage">
                        <Form.Label>Percentage for Bitcoin</Form.Label>
                        <Form.Select
                            value={percentage}
                            onChange={e => setPercentage(parseInt(e.target.value, 10))}
                            required
                        >
                            <option value="5">5%</option>
                            <option value="15">15%</option>
                            <option value="25">25%</option>
                            <option value="50">50%</option>
                            <option value="75">75%</option>
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>
            <Button variant="primary" type="submit" disabled={isLoading || !amount || !percentage}>
                {isLoading ? <Spinner as="span" animation="border" size="sm" /> : 'Preview Conversion'}
            </Button>
            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
        </Form>
    );
};

export default ConversionForm;
