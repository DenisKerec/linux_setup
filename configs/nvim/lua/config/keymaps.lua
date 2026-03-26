-- Keymaps are automatically loaded on the VeryLazy event

-- ─── File / Buffer Navigation ────────────────────────────────────────────────
vim.keymap.set("n", "<leader><leader>", "<cmd>FzfLua buffers<cr>", { desc = "Switch open buffers" })
vim.keymap.set("n", "<leader>sf", "<cmd>FzfLua files<cr>", { desc = "Search files" })
vim.keymap.set("n", "<leader>sg", "<cmd>FzfLua live_grep<cr>", { desc = "Search by grep" })
vim.keymap.set("n", "<leader>sw", "<cmd>FzfLua grep_cword<cr>", { desc = "Search word under cursor" })
vim.keymap.set("n", "<leader>sr", "<cmd>FzfLua oldfiles<cr>", { desc = "Search recent files" })
vim.keymap.set("n", "<leader>s.", "<cmd>FzfLua resume<cr>", { desc = "Resume last search" })

-- ─── LSP ─────────────────────────────────────────────────────────────────────
vim.keymap.set("n", "gd", vim.lsp.buf.definition, { desc = "Go to definition" })
vim.keymap.set("n", "gD", vim.lsp.buf.declaration, { desc = "Go to declaration" })
vim.keymap.set("n", "gr", "<cmd>FzfLua lsp_references<cr>", { desc = "Find references" })
vim.keymap.set("n", "gi", "<cmd>FzfLua lsp_implementations<cr>", { desc = "Find implementations" })
vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, { desc = "Code action" })
vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, { desc = "Rename symbol" })
vim.keymap.set("n", "K", vim.lsp.buf.hover, { desc = "Hover docs" })
vim.keymap.set("n", "<leader>d", vim.diagnostic.open_float, { desc = "Show diagnostics" })
vim.keymap.set("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
vim.keymap.set("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })

-- ─── Splits & Windows ────────────────────────────────────────────────────────
vim.keymap.set("n", "<C-h>", "<C-w>h", { desc = "Move to left window" })
vim.keymap.set("n", "<C-l>", "<C-w>l", { desc = "Move to right window" })
vim.keymap.set("n", "<C-j>", "<C-w>j", { desc = "Move to lower window" })
vim.keymap.set("n", "<C-k>", "<C-w>k", { desc = "Move to upper window" })

-- ─── Editing QoL ─────────────────────────────────────────────────────────────
vim.keymap.set("n", "<leader>nh", "<cmd>nohl<cr>", { desc = "Clear search highlight" })
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv", { desc = "Move selection down" })
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv", { desc = "Move selection up" })
vim.keymap.set("n", "<C-d>", "<C-d>zz", { desc = "Scroll down (centered)" })
vim.keymap.set("n", "<C-u>", "<C-u>zz", { desc = "Scroll up (centered)" })
vim.keymap.set("x", "<leader>p", '"_dP', { desc = "Paste without losing register" })
