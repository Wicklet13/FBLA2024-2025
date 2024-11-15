

(async function() {
    

    const labels = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    const data = {
        labels : labels,
        datasets : [{
            label: 'End of Month Balance',
            data: user['months'],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
            
    };
    //   { month: 'January', count: 10 },
    //   { month: 'February', count: 20 },
    //   { month: 'March', count: 15 },
    //   { month: 'April', count: 25 },
    //   { month: 'May', count: 22 },
    //   { month: 'June', count: 30 },
    //   { month: 'July', count: 28 },
    //   { month: 'August', count: 28 },
    //   { month: 'September', count: 28 },
    //   { month: 'October', count: 28 },
    //   { month: 'November', count: 28 },
    //   { month: 'December', count: 28 },
      
      


    new Chart(
      document.getElementById('acquisitions'),
      {
        type: 'line',
        
        data: data,
        
        options: {
            responsive : true,
            scales: {
                x: {
                    title: {
                    display: true,
                    text: 'Months',
                    }
                },
                
                y: {
                    beginAtZero: true,
                    title: {
                    display: true,
                    text: 'Balance In Dollars'
                    }
                }
            
            }
        }
        
    }
    );
  })();