document.addEventListener('DOMContentLoaded', () => {
  const statusElem = document.getElementById('status');
  const scanButton = document.getElementById('scan');

  // When the "Scan Website" button is clicked
  scanButton.addEventListener('click', () => {
    statusElem.textContent = 'Scanning...';

    // Send a message to the content script to start scanning
    chrome.runtime.sendMessage({ action: "check_website" }, (response) => {
      // Optionally handle the response if your content script sends one back
      if (response && response.result) {
        statusElem.textContent = response.result;
      } else {
        statusElem.textContent = 'Scan complete!';
      }
    });
  });
});
