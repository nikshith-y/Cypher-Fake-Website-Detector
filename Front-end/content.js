// Automatically execute the detection when the page loads
(function() {
    const currentUrl = window.location.href;
    
    // Replace 'https://your-api.com/detect' with your actual API endpoint.
    fetch(`http://127.0.0.1:5000/detect?url=${encodeURIComponent(currentUrl)}`)
      .then(response => response.json())
      .then(data => {
        if (data.is_fake) {
          alert("🚨 Warning: This website is potentially fake!");
        } else {
          alert("✅ This website looks safe.");
        }
      })
      .catch(error => {
        console.error("Error fetching detection API:", error);
        alert("Error scanning website. Please try again later.");
      });
  })();
  