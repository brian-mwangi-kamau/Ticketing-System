// 1 
document.addEventListener('DOMContentLoaded', function () {
    const ticketItems = document.querySelectorAll('.ticket-item');

    function filterTickets(status) {
      ticketItems.forEach(function (ticketItem) {
        const ticketStatus = ticketItem.querySelector('.status').innerText.toLowerCase();
        const shouldShow = status === 'all' || ticketStatus === status;
        
        ticketItem.classList.toggle('hidden', !shouldShow);
      });
    }

    document.querySelector('ul.column-links').addEventListener('click', function (event) {
      event.preventDefault();
      const target = event.target;
      if (target.tagName === 'A') {
        const status = target.dataset.status.toLowerCase().trim();
        filterTickets(status);
      }
    });

    filterTickets('all');
});


  // 2
document.addEventListener('DOMContentLoaded', function () {
    const ticketItems = document.querySelectorAll('.ticket-item');

    function showComments(ticketId) {
        console.log('Opening comments for ticket ID:', ticketId);
    }

    ticketItems.forEach(function (ticketItem) {
        ticketItem.addEventListener('click', function (event) {
        if (!event.target.closest('.ticket-item a, .ticket-item button, .ticket-item input')) {
            const ticketId = ticketItem.querySelector('.ticket_id').innerText.replace('#', '');
            showComments(ticketId);
        }
        });
    });
});