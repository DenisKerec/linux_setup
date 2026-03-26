-- Java + Spring Boot enhancements
return {
  -- Ensure treesitter parsers for Java + XML (Spring configs)
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}
      vim.list_extend(opts.ensure_installed, { "java", "xml" })
    end,
  },

  -- Mason: ensure Java debug/test tools are installed
  {
    "williamboman/mason.nvim",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}
      vim.list_extend(opts.ensure_installed, {
        "jdtls",
        "java-debug-adapter",
        "java-test",
      })
    end,
  },

  -- jdtls settings: Spring Boot completion favorites + inlay hints
  {
    "mfussenegger/nvim-jdtls",
    opts = function(_, opts)
      opts.settings = vim.tbl_deep_extend("force", opts.settings or {}, {
        java = {
          inlayHints = { parameterNames = { enabled = "all" } },
          signatureHelp = { enabled = true },
          contentProvider = { preferred = "fernflower" },
          format = { enabled = true },
          completion = {
            favoriteStaticMembers = {
              "org.assertj.core.api.Assertions.*",
              "org.junit.jupiter.api.Assertions.*",
              "org.mockito.Mockito.*",
              "org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*",
              "org.springframework.test.web.servlet.result.MockMvcResultMatchers.*",
            },
          },
        },
      })
      return opts
    end,
  },
}
