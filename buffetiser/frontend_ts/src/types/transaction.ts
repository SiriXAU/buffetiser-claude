/**
 * Transaction type definitions for purchases and sales.
 */

export type Currency = "AUD" | "USD" | "EUR" | "GBP" | "JPY" | "CNY";
export type Exchange = "ASX" | "NAS" | "NYS" | "LON" | "FRA" | "HKG" | "JPX";
export type Platform = "CMC" | "LINK" | "BOARDROOM" | "DIRECT" | "IPO";

export interface PurchaseCreate {
  symbol: string;
  units: number;
  price_per_unit: number;
  fee: number;
  date: string;
  currency?: Currency;
  exchange?: Exchange;
  platform?: Platform;
}

export interface Purchase {
  id: number;
  investment_id: number;
  units: number;
  price_per_unit: number;
  fee: number;
  date: string;
  trade_count: number;
  currency: string;
  exchange: string;
  platform: string;
  created_at: string;
  total_cost: number;
  cost_base_per_unit: number;
}

export interface SaleCreate {
  symbol: string;
  units: number;
  price_per_unit: number;
  fee: number;
  date: string;
  currency?: Currency;
  exchange?: Exchange;
}

export interface ParcelSelection {
  parcel_id: number;
  units_to_sell: number;
}

export interface SaleWithParcelSelection extends SaleCreate {
  parcel_selections: ParcelSelection[];
}

export interface Sale {
  id: number;
  investment_id: number;
  units: number;
  price_per_unit: number;
  fee: number;
  date: string;
  trade_count: number;
  currency: string;
  exchange: string;
  created_at: string;
  total_proceeds: number;
  proceeds_per_unit: number;
  capital_gain?: number;
  cgt_discount_applied: boolean;
  discounted_capital_gain?: number;
}
