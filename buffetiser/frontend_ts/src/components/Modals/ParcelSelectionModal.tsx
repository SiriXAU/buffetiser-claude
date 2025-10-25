/**
 * Parcel Selection Modal
 *
 * Allows users to select specific tax parcels when recording a sale
 * for tax optimization purposes.
 */

import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Table, Alert } from 'react-bootstrap';
import { api } from '../../api/client';
import { TaxParcel, ParcelSelection } from '../../types';
import './ParcelSelectionModal.css';

interface ParcelSelectionModalProps {
  show: boolean;
  onHide: () => void;
  investmentId: number;
  investmentSymbol: string;
  totalUnitsToSell: number;
  onConfirm: (selections: ParcelSelection[]) => void;
}

export const ParcelSelectionModal: React.FC<ParcelSelectionModalProps> = ({
  show,
  onHide,
  investmentId,
  investmentSymbol,
  totalUnitsToSell,
  onConfirm,
}) => {
  const [parcels, setParcels] = useState<TaxParcel[]>([]);
  const [selections, setSelections] = useState<Map<number, number>>(new Map());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (show) {
      loadParcels();
    }
  }, [show, investmentId]);

  const loadParcels = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.tax.getAvailableParcels(investmentId);
      setParcels(response.data.parcels);
      setSelections(new Map());
    } catch (err: any) {
      setError('Failed to load available parcels');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUnitsChange = (parcelId: number, units: number) => {
    const parcel = parcels.find((p) => p.id === parcelId);
    if (!parcel) return;

    const newSelections = new Map(selections);

    if (units <= 0 || isNaN(units)) {
      newSelections.delete(parcelId);
    } else {
      // Cap at available units
      const cappedUnits = Math.min(units, parcel.units_remaining);
      newSelections.set(parcelId, cappedUnits);
    }

    setSelections(newSelections);
  };

  const getTotalSelected = (): number => {
    return Array.from(selections.values()).reduce((sum, units) => sum + units, 0);
  };

  const getRemainingToSelect = (): number => {
    return totalUnitsToSell - getTotalSelected();
  };

  const getRecommendation = (parcel: TaxParcel): string => {
    const holdingDays = Math.floor(
      (new Date().getTime() - new Date(parcel.acquisition_date).getTime()) /
        (1000 * 60 * 60 * 24)
    );

    if (holdingDays >= 365) {
      return 'Long-term (50% CGT discount)';
    } else {
      const daysUntilDiscount = 365 - holdingDays;
      return `Short-term (${daysUntilDiscount} days until discount)`;
    }
  };

  const handleAutoSelectFIFO = () => {
    const newSelections = new Map<number, number>();
    let remaining = totalUnitsToSell;

    // Sort by acquisition date (oldest first)
    const sortedParcels = [...parcels].sort(
      (a, b) =>
        new Date(a.acquisition_date).getTime() -
        new Date(b.acquisition_date).getTime()
    );

    for (const parcel of sortedParcels) {
      if (remaining <= 0) break;

      const unitsToTake = Math.min(remaining, parcel.units_remaining);
      newSelections.set(parcel.id, unitsToTake);
      remaining -= unitsToTake;
    }

    setSelections(newSelections);
  };

  const handleAutoSelectOptimized = () => {
    const newSelections = new Map<number, number>();
    let remaining = totalUnitsToSell;

    // Prioritize long-term holdings (eligible for discount)
    const longTermParcels = parcels
      .filter((p) => {
        const holdingDays = Math.floor(
          (new Date().getTime() - new Date(p.acquisition_date).getTime()) /
            (1000 * 60 * 60 * 24)
        );
        return holdingDays >= 365;
      })
      .sort(
        (a, b) =>
          new Date(a.acquisition_date).getTime() -
          new Date(b.acquisition_date).getTime()
      );

    // Then short-term
    const shortTermParcels = parcels
      .filter((p) => {
        const holdingDays = Math.floor(
          (new Date().getTime() - new Date(p.acquisition_date).getTime()) /
            (1000 * 60 * 60 * 24)
        );
        return holdingDays < 365;
      })
      .sort(
        (a, b) =>
          new Date(a.acquisition_date).getTime() -
          new Date(b.acquisition_date).getTime()
      );

    // Select from long-term first
    for (const parcel of [...longTermParcels, ...shortTermParcels]) {
      if (remaining <= 0) break;

      const unitsToTake = Math.min(remaining, parcel.units_remaining);
      newSelections.set(parcel.id, unitsToTake);
      remaining -= unitsToTake;
    }

    setSelections(newSelections);
  };

  const handleConfirm = () => {
    const parcelSelections: ParcelSelection[] = Array.from(
      selections.entries()
    ).map(([parcel_id, units_to_sell]) => ({
      parcel_id,
      units_to_sell,
    }));

    onConfirm(parcelSelections);
    onHide();
  };

  const canConfirm = () => {
    const total = getTotalSelected();
    return Math.abs(total - totalUnitsToSell) < 0.0001;
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>
          Select Parcels to Sell - {investmentSymbol}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {loading ? (
          <div className="text-center py-4">
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : error ? (
          <Alert variant="danger">{error}</Alert>
        ) : (
          <>
            {/* Summary */}
            <Alert variant="info">
              <div className="d-flex justify-content-between">
                <div>
                  <strong>Total units to sell:</strong> {totalUnitsToSell}
                </div>
                <div>
                  <strong>Selected:</strong>{' '}
                  <span
                    className={
                      canConfirm() ? 'text-success' : 'text-warning'
                    }
                  >
                    {getTotalSelected().toFixed(4)}
                  </span>
                </div>
                <div>
                  <strong>Remaining:</strong>{' '}
                  <span
                    className={
                      getRemainingToSelect() === 0
                        ? 'text-success'
                        : 'text-danger'
                    }
                  >
                    {getRemainingToSelect().toFixed(4)}
                  </span>
                </div>
              </div>
            </Alert>

            {/* Auto-select buttons */}
            <div className="mb-3">
              <Button
                variant="outline-primary"
                size="sm"
                onClick={handleAutoSelectFIFO}
                className="me-2"
              >
                Auto-Select FIFO
              </Button>
              <Button
                variant="outline-success"
                size="sm"
                onClick={handleAutoSelectOptimized}
              >
                Auto-Select Optimized (Maximize CGT Discount)
              </Button>
            </div>

            {/* Parcels table */}
            <div className="table-responsive">
              <Table striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th>Acquired</th>
                    <th>Available Units</th>
                    <th>Cost Base/Unit</th>
                    <th>Tax Treatment</th>
                    <th>Units to Sell</th>
                  </tr>
                </thead>
                <tbody>
                  {parcels.map((parcel) => (
                    <tr key={parcel.id}>
                      <td>
                        {new Date(
                          parcel.acquisition_date
                        ).toLocaleDateString('en-AU')}
                      </td>
                      <td>{parcel.units_remaining.toFixed(4)}</td>
                      <td>${parcel.cost_base_per_unit.toFixed(2)}</td>
                      <td>
                        <small
                          className={
                            getRecommendation(parcel).includes('Long-term')
                              ? 'text-success'
                              : 'text-warning'
                          }
                        >
                          {getRecommendation(parcel)}
                        </small>
                      </td>
                      <td>
                        <Form.Control
                          type="number"
                          size="sm"
                          min="0"
                          max={parcel.units_remaining}
                          step="0.0001"
                          value={selections.get(parcel.id) || ''}
                          onChange={(e) =>
                            handleUnitsChange(
                              parcel.id,
                              parseFloat(e.target.value)
                            )
                          }
                          placeholder="0"
                        />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>

            {/* Help text */}
            <Alert variant="light" className="mt-3">
              <small>
                <strong>Tip:</strong> Selecting parcels held for 12+ months
                qualifies for the 50% CGT discount. The "Auto-Select Optimized"
                button prioritizes these parcels to minimize your tax liability.
              </small>
            </Alert>
          </>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancel
        </Button>
        <Button
          variant="primary"
          onClick={handleConfirm}
          disabled={!canConfirm()}
        >
          Confirm Selection
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
