// Statistic
document.addEventListener("DOMContentLoaded", function(event){
    let circle = document.querySelectorAll(".circle");
    circle.forEach(function(progress){
        let degree = 0;
        var targetDegree = parseInt(progress.getAttribute('data-degree'));
        let color = progress.getAttribute("data-color");
        let number = progress.querySelector(".number");

        var interval = setInterval(function(){
            degree += 1;
            if (degree > targetDegree) {
                clearInterval(interval);
                return;
                }
            progress.style.background = `conic-gradient(
                ${color} ${degree}%, #222 0%)`;
                number.innerHTML = degree + '<span>%</span>';
                number.style.color = color;
            }, 50)
        })
})



// Carousel
document.addEventListener('DOMContentLoaded', () => {
    let currentIndex = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    function showSlide(index) {
        document.querySelector('.carousel-slides').style.transform = `translateX(-${index * 100}%)`;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(currentIndex);
    }

    // Auto-slide every 10 seconds
    setInterval(nextSlide, 10000);

    // Initial display
    showSlide(currentIndex);
    document.querySelector('.prev').addEventListener('click', prevSlide);
    document.querySelector('.next').addEventListener('click', nextSlide);
});

// Feature Ranking
const correlations = {
    NGRDI: 24,
    ExGR: 23,
    VARI: 21,
    MGRVI: 17,
    GRRI: 16
};

// Generate a bar chart for feature importance using Plotly
function drawPlotlyChart(data) {
    const trace = {
        x: Object.keys(data),
        y: Object.values(data), 
        type: 'bar',
        marker: {
            color: 'rgba(28, 170, 95, 0.6)'
        }
        
    };
    

    const layout = {
        title: {
            text: 'Feature Importance',
            font: {
                family: "'Arkhip', sans-serif"
            }
        },
        xaxis: {
            title: {
                text: 'Indices',
                font: {
                    family: "'Arkhip', sans-serif"
                }
            },
            tickangle: -45,
            tickfont: {
                family: "'Arkhip', sans-serif"
            }
        },
        yaxis: {
            title: {
                text: 'Importance Value %',
                font: {
                    family: "'Arkhip', sans-serif"
                }
            },
            range: [0, 100],
            tickfont: {
                family: "'Arkhip', sans-serif"
            }
        },
        font: {
            family: "'Arkhip', sans-serif"
        },
        transition: {
            duration: 1000,
            easing: 'cubic-in-out'
        },
        barcornerradius: 15
        
    };
    
    // Configuration for initial rendering
    const config = {
        displayModeBar: false,
        responsive: true
    };

    // Plot the initial chart
    Plotly.newPlot('importanceChart', [trace], layout, config);

}

drawPlotlyChart(correlations);

