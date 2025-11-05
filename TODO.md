# TODO

- [x] Update `update_daily_changes` to accept the incoming request object; the current signature with no parameters causes Django to raise a `TypeError` when the endpoint is called. Also adjust `update_all_investments` to forward the request after the fix. 【F:buffetiser/backend/core/views.py†L36-L68】 ✅ **COMPLETED**
- [x] Fix `CronTimeView.post` to use the incoming `request` data instead of the undefined `response`, and supply a real timezone object to the scheduler rather than the plain string currently passed through. 【F:buffetiser/backend/core/views.py†L161-L195】 ✅ **COMPLETED**
- [x] Drop the unsupported `visible` keyword and any other unintended arguments when seeding the placeholder purchase in `NewInvestmentView`; the call currently crashes because the `Purchase` model has no such field. 【F:buffetiser/backend/core/views.py†L264-L306】【F:buffetiser/backend/core/models.py†L74-L116】 ✅ **COMPLETED**
- [x] Ensure dividend reinvestment requests include the required `price_per_unit`; the view presently omits it, so saving raises an integrity error on the mandatory field. 【F:buffetiser/backend/core/views.py†L447-L464】【F:buffetiser/backend/core/models.py†L129-L170】 ✅ **COMPLETED**
- [x] Add explicit `fields = "__all__"` declarations (or the desired subset) for every DRF `ModelSerializer`; without them DRF refuses to instantiate the serializer classes. 【F:buffetiser/backend/core/serializers.py†L13-L40】 ✅ **COMPLETED**
- [x] Harden the portfolio math helpers: avoid indexing `History` with `[1]` when fewer than two records exist, and guard the zero-divisions in the total cost/value calculations. 【F:buffetiser/backend/core/services/investment_details.py†L29-L125】 ✅ **COMPLETED**
- [x] Sort transactions in `ReportsView` using real dates instead of the `dd/mm/YYYY` strings so cross-month ordering stays correct. 【F:buffetiser/backend/core/views.py†L371-L396】 ✅ **COMPLETED**

## Summary

All TODO items have been successfully completed and committed. The backend should now be fully functional with all identified issues resolved.
