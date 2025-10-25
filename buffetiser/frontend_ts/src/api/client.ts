/**
 * API client with typed requests.
 */

import axios, { AxiosInstance } from 'axios';
import type {
  Investment,
  InvestmentCreate,
  InvestmentDetail,
  InvestmentUpdate,
  Purchase,
  PurchaseCreate,
  Sale,
  SaleCreate,
  SaleWithParcelSelection,
  CGTEvent,
  TaxReport,
  TaxParcel,
  AvailableParcelsResponse,
  CGTSummary,
} from '../types';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    });

    // Add request interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Investment endpoints
  investments = {
    getAll: (visibleOnly: boolean = true) =>
      this.client.get<Investment[]>('/investments', {
        params: { visible_only: visibleOnly },
      }),

    getById: (id: number) =>
      this.client.get<InvestmentDetail>(`/investments/${id}`),

    create: (data: InvestmentCreate) =>
      this.client.post<Investment>('/investments', data),

    update: (id: number, data: InvestmentUpdate) =>
      this.client.patch<Investment>(`/investments/${id}`, data),

    delete: (id: number) => this.client.delete(`/investments/${id}`),
  };

  // Transaction endpoints
  transactions = {
    createPurchase: (data: PurchaseCreate) =>
      this.client.post<Purchase>('/transactions/purchase', data),

    createSale: (data: SaleCreate) =>
      this.client.post<Sale>('/transactions/sale', data),

    createSaleWithParcels: (data: SaleWithParcelSelection) =>
      this.client.post<Sale>('/transactions/sale-with-parcels', data),

    getPurchases: (investmentId: number) =>
      this.client.get<Purchase[]>(`/transactions/${investmentId}/purchases`),

    getSales: (investmentId: number) =>
      this.client.get<Sale[]>(`/transactions/${investmentId}/sales`),
  };

  // Dividend endpoints
  dividends = {
    createPayment: (data: {
      symbol: string;
      value: number;
      date: string;
    }) => this.client.post('/dividends/payment', data),

    createReinvestment: (data: {
      symbol: string;
      units: number;
      price_per_unit: number;
      date: string;
    }) => this.client.post('/dividends/reinvestment', data),

    getPayments: (investmentId: number) =>
      this.client.get(`/dividends/${investmentId}/payments`),

    getReinvestments: (investmentId: number) =>
      this.client.get(`/dividends/${investmentId}/reinvestments`),
  };

  // Tax endpoints
  tax = {
    getEvents: (startDate: string, endDate: string, investmentId?: number) =>
      this.client.get<CGTEvent[]>('/tax/events', {
        params: {
          start_date: startDate,
          end_date: endDate,
          investment_id: investmentId,
        },
      }),

    getReport: (year: number) =>
      this.client.get<TaxReport>(`/tax/report/${year}`),

    getSummary: (year: number) =>
      this.client.get<CGTSummary>(`/tax/summary/${year}`),

    getAvailableParcels: (investmentId: number) =>
      this.client.get<AvailableParcelsResponse>(
        `/tax/parcels/${investmentId}`
      ),
  };

  // Export endpoints
  export = {
    taxCSV: async (startDate: string, endDate: string): Promise<Blob> => {
      const response = await this.client.get('/export/tax/csv', {
        params: { start_date: startDate, end_date: endDate },
        responseType: 'blob',
      });
      return response.data;
    },

    taxPDF: async (year: number): Promise<Blob> => {
      const response = await this.client.get(`/export/tax/pdf/${year}`, {
        responseType: 'blob',
      });
      return response.data;
    },
  };

  // Portfolio endpoints
  portfolio = {
    getSummary: () => this.client.get('/portfolio/summary'),
    getHistory: () => this.client.get('/portfolio/history'),
  };
}

export const api = new ApiClient();
export default api;
