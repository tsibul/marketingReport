const path = require('path');

module.exports = {
  entry: {
    login: './marketing_report/static/marketing_report/js/login.js',
    index: './marketing_report/static/marketing_report/js/index.js',
    customer: './marketing_report/static/marketing_report/js/customer.js',
    main: './marketing_report/static/marketing_report/js/main.js',
    imports: './marketing_report/static/marketing_report/js/imports.js',
    dictionary: './marketing_report/static/marketing_report/js/dictionary.js',
    report_page: './marketing_report/static/marketing_report/js/report_page.js',
    admin: './marketing_report/static/marketing_report/js/admin.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'marketing_report/static/marketing_report/js/dist'),
    clean: true,
  },
  mode: "production",
};