document.addEventListener('DOMContentLoaded', () => {
    // Donation amount selection
    const amountBtns = document.querySelectorAll('.amount-btn');
    amountBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            amountBtns.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });

    // Crypto address copy
    const cryptoAddresses = document.querySelectorAll('.crypto-option code');
    cryptoAddresses.forEach(address => {
        address.addEventListener('click', () => {
            navigator.clipboard.writeText(address.textContent).then(() => {
                alert('Address copied to clipboard!');
            });
        });
    });

    // Fund Allocation Chart
    const ctx = document.getElementById('fundAllocationChart').getContext('2d');
    const fundAllocationChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Development', 'Infrastructure', 'Community Support', 'Marketing & Outreach', 'Miscellaneous'],
            datasets: [{
                data: [45, 25, 15, 10, 5],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF'
                ],
                hoverBackgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Fund Allocation Breakdown'
                }
            }
        }
    });
});

// Navbar dropdown functionality
const navDropdowns = document.querySelectorAll('.dropdown');

navDropdowns.forEach(dropdown => {
    const dropbtn = dropdown.querySelector('.dropbtn');
    const dropdownContent = dropdown.querySelector('.dropdown-content');

    dropbtn.addEventListener('click', (e) => {
        e.preventDefault();
        dropdown.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });
});