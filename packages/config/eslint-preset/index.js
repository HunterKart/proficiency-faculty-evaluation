import tseslint from "typescript-eslint";
import reactPlugin from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config(
  [
    {
      ignores: ["dist", "node_modules"]
    }
  ],
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.json"],
        tsconfigRootDir: import.meta.dirname
      }
    },
    extends: [
      ...tseslint.configs.recommendedTypeChecked,
      ...tseslint.configs.stylisticTypeChecked,
      reactPlugin.configs["recommended-typescript"],
      reactDom.configs.recommended
    ],
    settings: {
      react: {
        version: "detect"
      }
    }
  }
);
