/**
 * Tax Report Table Component
 *
 * Displays CGT events in a sortable table with full details.
 */

import React, { useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
  createColumnHelper,
  SortingState,
} from '@tanstack/react-table';
import { CGTEvent } from '../../types';
import './TaxReportTable.css';

interface TaxReportTableProps {
  events: CGTEvent[];
}

const columnHelper = createColumnHelper<CGTEvent>();

export const TaxReportTable: React.FC<TaxReportTableProps> = ({ events }) => {
  const [sorting, setSorting] = React.useState<SortingState>([
    { id: 'disposal_date', desc: true }, // Default: newest first
  ]);

  const columns = useMemo(
    () => [
      columnHelper.accessor('disposal_date', {
        header: 'Date',
        cell: (info) => new Date(info.getValue()).toLocaleDateString('en-AU', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
        }),
      }),
      columnHelper.accessor('investment_symbol', {
        header: 'Investment',
        cell: (info) => (
          <strong>{info.getValue()}</strong>
        ),
      }),
      columnHelper.accessor('units_sold', {
        header: 'Units',
        cell: (info) => info.getValue().toFixed(4),
      }),
      columnHelper.accessor('holding_period_days', {
        header: 'Held (Days)',
        cell: (info) => (
          <span className={info.getValue() >= 365 ? 'text-success' : 'text-warning'}>
            {info.getValue()}
          </span>
        ),
      }),
      columnHelper.accessor('acquisition_date', {
        header: 'Acquired',
        cell: (info) => new Date(info.getValue()).toLocaleDateString('en-AU', {
          day: '2-digit',
          month: 'short',
          year: 'numeric',
        }),
      }),
      columnHelper.accessor('cost_base', {
        header: 'Cost Base',
        cell: (info) => `$${info.getValue().toFixed(2)}`,
      }),
      columnHelper.accessor('proceeds', {
        header: 'Proceeds',
        cell: (info) => `$${info.getValue().toFixed(2)}`,
      }),
      columnHelper.accessor('capital_gain', {
        header: 'Capital Gain',
        cell: (info) => {
          const value = info.getValue();
          return (
            <span className={value >= 0 ? 'text-success fw-bold' : 'text-danger fw-bold'}>
              ${value.toFixed(2)}
            </span>
          );
        },
      }),
      columnHelper.accessor('cgt_discount_applied', {
        header: 'CGT Discount',
        cell: (info) => (
          <span className={info.getValue() ? 'badge bg-success' : 'badge bg-secondary'}>
            {info.getValue() ? '50%' : '0%'}
          </span>
        ),
      }),
      columnHelper.accessor('discount_amount', {
        header: 'Discount $',
        cell: (info) => {
          const value = info.getValue();
          return value > 0 ? (
            <span className="text-success">-${value.toFixed(2)}</span>
          ) : (
            <span className="text-muted">$0.00</span>
          );
        },
      }),
      columnHelper.accessor('net_capital_gain', {
        header: 'Net Gain',
        cell: (info) => {
          const value = info.getValue();
          return (
            <span className={value >= 0 ? 'text-success fw-bold' : 'text-danger fw-bold'}>
              ${value.toFixed(2)}
            </span>
          );
        },
      }),
    ],
    []
  );

  const table = useReactTable({
    data: events,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  if (events.length === 0) {
    return (
      <div className="alert alert-info">
        No CGT events found for this period.
      </div>
    );
  }

  return (
    <div className="tax-report-table-container">
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark sticky-top">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    onClick={header.column.getToggleSortingHandler()}
                    style={{ cursor: 'pointer', userSelect: 'none' }}
                  >
                    <div className="d-flex align-items-center justify-content-between">
                      {flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                      <span className="ms-2">
                        {{
                          asc: '↑',
                          desc: '↓',
                        }[header.column.getIsSorted() as string] ?? '⇅'}
                      </span>
                    </div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="table-footer text-muted mt-2">
        <small>
          Showing {events.length} CGT event{events.length !== 1 ? 's' : ''}
        </small>
      </div>
    </div>
  );
};
