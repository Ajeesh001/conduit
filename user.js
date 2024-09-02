

document.getElementById('yourfeed-link').addEventListener('click', function(event) {
    event.preventDefault(); 
    document.getElementById('yourfeed-content').style.display = 'block';
    document.getElementById('globalfeed-content').style.display = 'none';
});

document.getElementById('globalfeed-link').addEventListener('click', function(event) {
    event.preventDefault(); 
    document.getElementById('yourfeed-content').style.display = 'none';
    document.getElementById('globalfeed-content').style.display = 'block';
});




