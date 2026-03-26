-- SQL: dadbod for live DB connections + sqlls (Node-based LSP, no Go required)
return {
  -- Use sqlls (Node.js) instead of sqls (requires Go)
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        sqlls = {},
      },
    },
  },

  {
    "williamboman/mason.nvim",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}
      vim.list_extend(opts.ensure_installed, { "sqlls" })
    end,
  },

  {
    "kristijanhusak/vim-dadbod-ui",
    dependencies = {
      { "tpope/vim-dadbod", lazy = true },
      { "kristijanhusak/vim-dadbod-completion", ft = { "sql", "mysql", "plsql" }, lazy = true },
    },
    cmd = { "DBUI", "DBUIToggle", "DBUIAddConnection", "DBUIFindBuffer" },
    keys = {
      { "<leader>Du", "<cmd>DBUIToggle<cr>", desc = "Toggle DB UI" },
      { "<leader>Da", "<cmd>DBUIAddConnection<cr>", desc = "Add DB connection" },
      { "<leader>Df", "<cmd>DBUIFindBuffer<cr>", desc = "Find DB buffer" },
    },
    init = function()
      vim.g.db_ui_use_nerd_fonts = 1
      vim.g.db_ui_save_location = vim.fn.stdpath("data") .. "/db_ui"
    end,
  },
}
