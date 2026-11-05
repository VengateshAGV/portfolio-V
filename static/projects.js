window.PROJECTS = [
  {
    id: "ninjatrader-suite",
    icon: "📊",
    title: "NinjaTrader Multi-Strategy Suite",
    short: "Custom NinjaScript Indicators, Strategies, and AddOns with multi-timeframe logic, order management, and ATM templates.",
    tags: ["C#", "NinjaScript", "NT8"],
    result: "Multiple strategies running with validated backtest → live parity.",
    repo: "https://github.com/VengateshAGV",
    problem: "Needed reliable, automated multi-timeframe strategies inside NinjaTrader with consistent order management and repeatable ATM setups.",
    built: [
      "Custom Indicators in NinjaScript (C#) for multi-timeframe signals",
      "Strategies with automated order management and risk controls",
      "AddOns for shared state, UI panels, and execution hooks",
      "ATM templates configured for consistent position sizing"
    ],
    stack: ["C#", "NinjaScript", "NinjaTrader 8"],
    metrics: [
      ["Strategies deployed", "Multiple"],
      ["Backtest → live parity", "Validated"],
      ["Order routing", "Native NT8"]
    ]
  },
  {
    id: "tradingview-pack",
    icon: "📈",
    title: "TradingView Pine Script Pack",
    short: "Custom indicators and alert-ready strategies in Pine Script v5, wired to webhook execution pipelines.",
    tags: ["Pine v5", "Webhooks", "Alerts"],
    result: "Indicators + strategies with live webhook → bot execution.",
    repo: "https://github.com/VengateshAGV",
    problem: "Needed TradingView indicators that fire reliable alerts and trigger execution downstream via webhooks.",
    built: [
      "Custom Pine Script v5 indicators",
      "Alert conditions wired to webhook endpoints",
      "Strategies with entry/exit logic and backtest-friendly code",
      "Webhook payload schema for downstream bot consumption"
    ],
    stack: ["Pine Script v5", "TradingView", "Webhooks"],
    metrics: [
      ["Indicators built", "Multiple"],
      ["Alert delivery", "Real-time webhooks"],
      ["Platform", "TradingView"]
    ]
  },
  {
    id: "multi-exchange-bot",
    icon: "🤖",
    title: "Multi-Exchange Auto-Trading Bot",
    short: "Unified execution layer across IBKR, BitMart, BitUnix, Coinbase, and Sunperp using REST + WebSocket connectors.",
    tags: ["Python", "REST", "WebSocket", "IBKR"],
    result: "Single bot controlling 5 exchanges with low-latency order routing.",
    repo: "https://github.com/VengateshAGV",
    problem: "Fragmented execution across multiple brokers/exchanges made strategy deployment slow and error-prone.",
    built: [
      "Unified execution layer abstracting 5+ exchange APIs",
      "REST + WebSocket connectors for low-latency order routing",
      "Position and risk management across accounts",
      "Retry, reconciliation, and error-handling logic"
    ],
    stack: ["Python", "REST", "WebSocket", "IBKR API", "BitMart", "BitUnix", "Coinbase", "Sunperp"],
    metrics: [
      ["Exchanges integrated", "5+"],
      ["Order routing", "<100ms (tested)"],
      ["Transport", "REST + WebSocket"]
    ]
  },
  {
    id: "signal-engine",
    icon: "💬",
    title: "Telegram/Discord Signal Engine",
    short: "Receives trading signals via Telegram/Discord webhooks, auto-executes trades, and posts real-time status updates back to channels.",
    tags: ["Python", "Telegram Bot API", "Discord"],
    result: "End-to-end signal → execution → status tracking, automated.",
    repo: "https://github.com/VengateshAGV",
    problem: "Manual signal relay from chat channels to execution was slow and untrackable.",
    built: [
      "Telegram + Discord signal ingestion (get)",
      "Automatic trade execution on signal match",
      "Status posting back to channels (post)",
      "Signal log and status tracker"
    ],
    stack: ["Python", "Telegram Bot API", "Discord Webhooks"],
    metrics: [
      ["Signal delivery", "Near real-time"],
      ["Channels", "Telegram + Discord"],
      ["Tracking", "Status posted per event"]
    ]
  },
  {
    id: "options-automator",
    icon: "🎯",
    title: "Options Strategy Automator",
    short: "Automated Iron Butterfly and customizable multi-leg options setups with execution logic and risk controls.",
    tags: ["Python", "IBKR API", "Options"],
    result: "Multi-leg execution with customizable templates.",
    repo: "https://github.com/VengateshAGV",
    problem: "Multi-leg options setups were slow to build and error-prone to execute manually.",
    built: [
      "Iron Butterfly automated execution model",
      "Customizable multi-leg option setup templates",
      "Risk controls and position sizing",
      "IBKR API integration for order placement"
    ],
    stack: ["Python", "IBKR API", "Options strategies"],
    metrics: [
      ["Strategy types", "Iron Butterfly + multi-leg"],
      ["Execution", "Automated via IBKR API"],
      ["Templates", "Customizable"]
    ]
  },
  {
    id: "backtest-pipeline",
    icon: "🔬",
    title: "Backtesting & Dry-Run Pipeline",
    short: "Validation framework comparing backtest vs live performance, with continuous dry-run testing and AI-assisted debugging.",
    tags: ["Python", "pandas", "LightGBM"],
    result: "Backtest-to-live parity validation across all deployed strategies.",
    repo: "https://github.com/VengateshAGV",
    problem: "Strategies that looked good in backtest failed in live — needed a rigorous validation pipeline.",
    built: [
      "Backtest vs live comparison framework",
      "Continuous dry-run validation structure",
      "Metrics reporting (win-rate, drawdown, latency)",
      "AI-assisted debugging for faster iteration"
    ],
    stack: ["Python", "pandas", "LightGBM", "AI-assisted tools"],
    metrics: [
      ["Validation", "Backtest vs live parity"],
      ["Dry-run", "Continuous"],
      ["Reporting", "Metrics per strategy"]
    ]
  }
];