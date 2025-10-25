/**
 * Tax type definitions for CGT reporting and parcel tracking.
 */

export type CGTTreatment = "short_term" | "long_term";

export interface TaxParcel {
  id: number;
  investment_id: number;
  acquisition_date: string;
  units_acquired: number;
  units_remaining: number;
  cost_base_per_unit: number;
  total_cost_base: number;
  description: string | null;
  is_fully_sold: boolean;
  percentage_remaining: number;
  created_at: string;
  updated_at: string;
}

export interface CGTEvent {
  id: number;
  event_date: string;
  financial_year: string;
  investment_symbol: string;
  investment_name: string | null;
  units_sold: number;
  acquisition_date: string;
  disposal_date: string;
  cost_base: number;
  proceeds: number;
  capital_gain: number;
  holding_period_days: number;
  cgt_treatment: CGTTreatment;
  cgt_discount_applied: boolean;
  discount_amount: number;
  net_capital_gain: number;
  sale_id: number;
  parcel_id: number | null;
}

export interface CGTSummary {
  financial_year: string;
  total_capital_gains: number;
  total_capital_losses: number;
  total_discount_amount: number;
  net_capital_gain: number;
  short_term_gains: number;
  long_term_gains: number;
  long_term_discounted: number;
  total_events: number;
  short_term_events: number;
  long_term_events: number;
  gains_by_investment: Record<string, number>;
}

export interface TaxReport {
  financial_year: string;
  report_generated: string;
  events: CGTEvent[];
  summary: CGTSummary;
  total_investments: number;
  date_range: {
    start: string;
    end: string;
  };
}

export interface AvailableParcelsResponse {
  investment_id: number;
  investment_symbol: string;
  total_units_available: number;
  parcels: TaxParcel[];
}
