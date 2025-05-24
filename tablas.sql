
-- Tabla de Ciclos
CREATE TABLE cycles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP NULL,
    target_usdt DECIMAL(15,8) NOT NULL,
    purchased_usdt DECIMAL(15,8) DEFAULT 0,
    sold_usdt DECIMAL(15,8) DEFAULT 0,
    total_invested DECIMAL(15,2) DEFAULT 0,
    total_returned DECIMAL(15,2) DEFAULT 0,
    total_profit DECIMAL(15,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'activo' CHECK (status IN ('activo', 'completado')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Transacciones
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    cycle_id INTEGER NOT NULL REFERENCES cycles(id) ON DELETE CASCADE,
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('compra', 'venta')),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Campos para compras
    usdt_desired DECIMAL(15,8) NULL,
    commission_rate DECIMAL(5,2) NULL,
    purchase_price DECIMAL(15,4) NULL,
    usdt_to_pay DECIMAL(15,8) NULL,
    total_investment_bs DECIMAL(15,2) NULL,
    real_purchase_price DECIMAL(15,4) NULL,
    buy_status VARCHAR(20) NULL CHECK (buy_status IN ('pendiente', 'completado')),
    
    -- Campos para ventas
    market_best_price DECIMAL(15,4) NULL,
    competitive_adjustment DECIMAL(15,4) NULL,
    sale_price DECIMAL(15,4) NULL,
    usdt_sold DECIMAL(15,8) NULL,
    profit_bs DECIMAL(15,2) NULL,
    profit_percentage DECIMAL(8,4) NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de vinculación entre ventas y compras (para rastrear qué compras se vendieron)
CREATE TABLE transaction_links (
    id SERIAL PRIMARY KEY,
    sell_transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    buy_transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    linked_amount DECIMAL(15,8) NOT NULL,
    buy_price DECIMAL(15,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
