module.exports = {
  assetsDir:
    process.env.NODE_ENV === "development"
      ? "http://localhost:8081/"
      : "../static",
  publicPath: "/",
  outputDir: "../api/templates",
  transpileDependencies: ["vuetify"]
};
