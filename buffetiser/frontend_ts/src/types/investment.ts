/**
 * Investment type definitions.
 */

export interface Investment {
  id: number;
  key: string;
  symbol: string;
  name: string | null;
  type: "Shares" | "Crypto";
  live_price: number;
  visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface InvestmentDetail extends Investment {
  units_held: number;
  average_cost: number;
  total_cost: number;
  current_value: number;
  total_profit: number;
  total_profit_percent: number;
  daily_change: number;
  daily_change_percent: number;
  price_history: PriceHistory[];
}

export interface PriceHistory {
  date: string;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface InvestmentCreate {
  symbol: string;
  name?: string;
  type?: "Shares" | "Crypto";
  exchange: string;
}

export interface InvestmentUpdate {
  name?: string;
  live_price?: number;
  visible?: boolean;
}
