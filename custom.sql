SELECT status,
       SUM(balance) / 100 AS total_deposit_balance,
       COUNT(*) AS all_cards_count,
       SUM(CASE WHEN balance < 0 THEN balance ELSE 0 END) / 100 AS negative_balances,
       COUNT(CASE WHEN balance < 0 THEN 1 END) AS count_negative_balances,
       SUM(CASE WHEN balance >= 0 AND balance <= 6500 THEN balance ELSE 0 END) / 100 AS balances_0_to_6500,
       COUNT(CASE WHEN balance >= 0 AND balance <= 6500 THEN 1 END) AS count_balances_0_to_6500,
       SUM(CASE WHEN balance > 6500 THEN balance ELSE 0 END) / 100 AS balances_above_6500,
       COUNT(CASE WHEN balance > 6500 THEN 1 END) AS count_balances_above_6500
FROM card
WHERE client_id IS NOT NULL
GROUP BY status;


Select count(*) from card where status='ACTIVE' and balance >=0 and balance <6500 and client_id is not null;
