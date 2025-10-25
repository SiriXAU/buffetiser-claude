/**
 * Central export for all types.
 */

export * from './investment';
export * from './transaction';
export * from './tax';

export interface ApiError {
  detail: string;
}

export interface ApiResponse<T> {
  data: T;
}
