function updateJuniorZoneDataset() {
    var urlCSV = 'https://raw.githubusercontent.com/Moscarde/Junior_Zone/main/data/googlesheets_dataset.csv';
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = spreadsheet.getSheetByName('raw_data');
  
    sheet.clear();
  
    var dataCSV = Utilities.parseCsv(UrlFetchApp.fetch(urlCSV).getContentText());
    sheet.getRange(1, 1, dataCSV.length, dataCSV[0].length).setValues(dataCSV);
  }