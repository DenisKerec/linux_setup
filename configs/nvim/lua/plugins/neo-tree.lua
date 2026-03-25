-- Override Neo-tree config (LazyVim includes neo-tree by default)
-- Preserving your Ctrl+N toggle keybinding from old config
return {
  "nvim-neo-tree/neo-tree.nvim",
  keys = {
    { "<C-n>", "<leader>fe", desc = "NeoTree toggle", remap = true },
  },
}
