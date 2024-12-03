import psycopg2
DB_URL = 'postgresql://default:2ytpuU7swTql@ep-young-salad-a10bjpmp-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require'
POSTGRES_URL="postgres://default:2ytpuU7swTql@ep-young-salad-a10bjpmp-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
POSTGRES_PRISMA_URL="postgres://default:2ytpuU7swTql@ep-young-salad-a10bjpmp-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require&pgbouncer=true&connect_timeout=15"
POSTGRES_URL_NO_SSL="postgres://default:2ytpuU7swTql@ep-young-salad-a10bjpmp-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb"
POSTGRES_URL_NON_POOLING="postgres://default:2ytpuU7swTql@ep-young-salad-a10bjpmp.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
POSTGRES_USER="default"
POSTGRES_HOST="ep-young-salad-a10bjpmp-pooler.ap-southeast-1.aws.neon.tech"
POSTGRES_PASSWORD="2ytpuU7swTql"
POSTGRES_DATABASE="verceldb"

def get_database_conn():
    try:
        conn = psycopg2.connect(
            DB_URL
        )
        print("Database Connected!")

        return conn
    
    except Exception as e:
        print("Database Connection Error:", e)
        return None
