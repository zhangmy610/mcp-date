from enum import Enum

class DbTypeAgentUrlMode(str, Enum):
    LOGIN_IN_URL = "{}/gateway/login_in"
    GET_DBID_BY_ALIAS_URL = "{}/gateway/monitor-interactive-service/db-monitor-config/list-by-page"
    GET_OPTIMIZATION_SUGGESTIONS_URL = "{}/gateway/monitor-interactive-service/database/sql-optimization/get-optimization-suggestions"
    SQL_AUDIT_LOGIN_IN_URL = "http://192.168.12.86:8960/gateway/login_in"
    SQL_AUDIT_TEMPLATE_ID_URL = "http://192.168.12.86:8960/gateway/sql-audit-service/template/page?pageSize=1000&pageNum=1&searchKey=defaultStatus&searchVal=1&dbProduct={}"
    SQL_AUDIT_URL = "http://192.168.12.86:8960/gateway/sql-audit-service/sql/quick_audit"
    SUBMIT_INSPECTION_URL = "{}/gateway/monitor-interactive-service/inspection/intelligent-inspection/submit-inspection-task"
    INSPECTION_STATUS_URL = "{}/gateway/monitor-interactive-service/inspection/history/query-inspection-task-info"
    INSPECTION_DETAIL_URL = "{}/gateway/monitor-interactive-service/inspection/history/query-inspection-task-item-info"
    INSPECTION_HEALTH_SCORE_URL = "{}/gateway/monitor-interactive-service/inspection/history/query-inspection-task-db-info?taskId={}&page=1&limit=15"

    ORACLE_CAPACITY_URL = "{}/gateway/monitor-interactive-service/database/oracle/capacity/capacity-info?dbid={}"
    ORACLE_CAPACITY_HISTORY_URL = "{}/gateway/monitor-interactive-service/database/oracle/capacity/capacity-and-used-ratio?dbid={}&startTime={}&endTime={}"
    ORACLE_INST_LIST_URL = "{}/gateway/monitor-interactive-service/database/oracle/inst-manage/get-inst-list?dbid={}"
    ORACLE_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/oracle/perf-analysis/workload/conn-chart?dbid={}&startTime={}&endTime={}&instId={}"
    ORACLE_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/oracle/perf-analysis/workload/qps-chart?dbid={}&startTime={}&endTime={}&instId={}"
    ORACLE_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/oracle/perf-analysis/workload/tps-chart?dbid={}&startTime={}&endTime={}&instId={}"
    ORACLE_SLOW_SQL_URL = "{}/gateway/monitor-interactive-service/database/oracle/perf-analysis/sql-analysis/get-top-sql?dbid={}&searchValue=&searchKey=INST_ID&searchType=0&limit=5&offset=0&startTime={}&endTime={}&sort=desc&term=AVG_EXLAPSED&monitorSql=N"
    ORACLE_SLOW_SQL_ORIGINAL_URL = "{}/gateway/monitor-interactive-service/database/oracle/perf-analysis/sql-analysis/get-text-by-sql-hash-id?sqlHashId={}&dbid={}"

    MYSQL_CAPACITY_URL = "{}/gateway/monitor-interactive-service/database/mysql/capacity/capacity-info?dbid={}"
    MYSQL_CAPACITY_HISTORY_URL = "{}/gateway/monitor-interactive-service/database/mysql/capacity/capacity-trend?dbid={}&startTime={}&endTime={}"
    MYSQL_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/mysql/perf-analysis/conn-num?dbid={}&startTime={}&endTime={}"
    MYSQL_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/mysql/perf-analysis/qps?dbid={}&startTime={}&endTime={}"
    MYSQL_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/mysql/perf-analysis/tps?dbid={}&startTime={}&endTime={}"
    MYSQL_SLOW_SQL_URL = "{}/gateway/monitor-interactive-service/database/mysql/perf-analysis/top-sql-list?dbid={}&startTime={}&endTime={}&limit=5&offset=0&pullDown=DIGEST&content=&compareType=20&search=SCHEMA_NAME&searchValue=&sort=DESC&term=CURR_AVG_TIMER_WAIT&monitorSql=N"
    MYSQL_SQL_ORIGINAL_URL = "{}/gateway/monitor-interactive-service/database/mysql/perf-analysis/original/sql?sqlHashId={}&dbid={}"

    OCEANBASE_CAPACITY_HISTORY_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/capacity-manage/all-tenant/capacity-use-ratio?dbid={}&startTime={}&endTime={}"
    OCEANBASE_SLOW_SQL_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/top-sql-tables?dbid={}&startTime={}&endTime={}&limit=5&offset=0&pullDown=DB_ID&content=&top=&compareSize=0&sort=DESC&term=AVG_ELAPSED_TIME&monitor=N&period=download"
    OCEANBASE_TENANT_TYPE_URL = "{}/gateway/monitor-interactive-service/asset-db/query-by-id?dbid={}"
    OCEANBASE_TENANT_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/member?dbid={}"

    OCEANBASE_ORACLE_CAPACITY_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/capacity-manage/oracle/capacity-base-info?dbid={}"
    OCEANBASE_ORACLE_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/oracle/workload/conn-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}"
    OCEANBASE_ORACLE_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/oracle/workload/sql-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}&type=qps"
    OCEANBASE_ORACLE_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/oracle/workload/transaction-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}&type=tps"

    OCEANBASE_MYSQL_CAPACITY_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/capacity-manage/mysql/capacity-base-info?dbid={}"
    OCEANBASE_MYSQL_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/mysql/workload/conn-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}"
    OCEANBASE_MYSQL_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/mysql/workload/sql-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}&type=qps"
    OCEANBASE_MYSQL_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/mysql/workload/transaction-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}&type=tps"

    OCEANBASE_SYS_SLOW_SQL_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/top-sql-tables?dbid={}&startTime={}&endTime={}&limit=5&offset=0&pullDown=DB_ID&content=&top=&compareSize=0&sort=DESC&term=AVG_ELAPSED_TIME&monitor=N&period=download&object_name=1"
    OCEANBASE_SYS_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/sys/workload/conn-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}"
    OCEANBASE_SYS_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/sys/workload/sql-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}&type=qps"
    OCEANBASE_SYS_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/oceanbase/perf-analysis/sys/workload/transaction-chart?dbid={}&startTime={}&endTime={}&object_type={}&object_name={}&type=tps"


    GAUSSDB_OG_CENTRALIZED_CAPACITY_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/capacity-management/capacity-info?dbid={}"
    GAUSSDB_OG_CENTRALIZED_CAPACITY_HISTORY_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/capacity-management/capacity-trend?dbid={}&startTime={}&endTime={}"
    GAUSSDB_OG_CENTRALIZED_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/perf-analysis/conn-num?dbid={}&startTime={}&endTime={}"
    GAUSSDB_OG_CENTRALIZED_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/perf-analysis/qps?dbid={}&startTime={}&endTime={}"
    GAUSSDB_OG_CENTRALIZED_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/perf-analysis/tps?dbid={}&startTime={}&endTime={}"
    GAUSSDB_OG_CENTRALIZED_SLOW_SQL_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/perf-analysis/top-sql?dbid={}&startTime={}&endTime={}&limit=5&offset=0&orderType=desc&orderColumn=AVG_DB_TIME&searchVal=&searchName=UNIQUE_SQL_ID&search=USER_NAME&searchValue=&flag=like"
    GAUSSDB_OG_CENTRALIZED_SQL_ORIGINAL_URL = "{}/gateway/monitor-interactive-service/database/gaussdb-central/perf-analysis/sql-text?sqlId={}&dbid={}"

    GOLDENDB_CAPACITY_URL = "{}/gateway/monitor-interactive-service/database/goldendb/capacity/capacity-info?dbid={}"
    GOLDENDB_CAPACITY_HISTORY_URL = "{}/gateway/monitor-interactive-service/database/goldendb/capacity/capacity-trend?dbid={}&startTime={}&endTime={}"
    GOLDENDB_PERFORMANCE_CONN_URL = "{}/gateway/monitor-interactive-service/database/goldendb/perf-analysis/conn-num?dbid={}&startTime={}&endTime={}"
    GOLDENDB_PERFORMANCE_QPS_URL = "{}/gateway/monitor-interactive-service/database/goldendb/perf-analysis/qps?dbid={}&startTime={}&endTime={}"
    GOLDENDB_PERFORMANCE_TPS_URL = "{}/gateway/monitor-interactive-service/database/goldendb/perf-analysis/tps?dbid={}&startTime={}&endTime={}"
    GOLDENDB_SLOW_SQL_URL = "{}/gateway/monitor-interactive-service/database/goldendb/perf-analysis/top-sql-list?dbid={}&startTime={}&endTime={}&limit=5&offset=0&pullDown=DIGEST&content=&compareType=20&search=SCHEMA_NAME&searchValue=&sort=DESC&term=CURR_AVG_TIMER_WAIT&monitorSql=N"
    GOLDENDB_SQL_ORIGINAL_URL = "{}/gateway/monitor-interactive-service/database/goldendb/perf-analysis/original/sql?sqlHashId={}&dbid={}"

class DbTypeAgentMode(str, Enum):
    ORACLE = "oracle"
    MYSQL = "mysql"
    OCEANBASE = "oceanbase"
    GAUSSDB_OG_CENTRALIZED = "gaussdb_og_centralized"
    GOLDENDB = "goldendb"