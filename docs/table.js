/* Formatting function for row details - modify as you need */
function format ( d ) {

    papers = 
    '<tr>'+
    '<td><span style="font-weight:bold">Venue</span></td>'+
    '<td><span style="font-weight:bold">Year</span></td>'+
    '<td><span style="font-weight:bold">Title</span></td>'+
    '<td><span style="font-weight:bold">Authors</span></td>'+
    '<td><span style="font-weight:bold">Citations</span></td>'+
    '</tr>';

    for (var i = 0; i < d.papers.length; i++){
        var paper = d.papers[i];
        papers +=
          '<tr>'+
          '<td>'+paper.venue+'</td>'+
          '<td>'+paper.year+'</td>'+
          '<td>'+paper.title+'</td>'+
          '<td>'+paper.authors+'</td>'+
          '<td>'+paper.citations+'</td>'+
          '</tr>';
    }

    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
            papers+
           '</table>';
}

$(document).ready(function() {
    var table = $('#example').DataTable({
        //'ajax': 'https://api.myjson.com/bins/16lp6',
        //'ajax': 'fakeauthorlist.json',
        'ajax': 'data.json',
        'columns': [
            {
                'className':      'details-control',
                'orderable':      false,
                'data':           null,
                'defaultContent': ''
            },
            { 'data': 'name' },
            { 'data': 'institution' },
            { 'data': 'bolsa-cnpq' },
            { 'data': 'num-top-papers' },
            { 'data': 'num-csindexbr-papers' },
            { 'data': 'num-csindexbr-journals' },
            { 'data': 'num-csindexbr-confs' },
            { 'data': 'csindexbr-score' }
        ],
        'order': [[4, 'desc']],
        'pageLength': 20
    } );

    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function(){
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if(row.child.isShown()){
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });

    // Handle click on "Expand All" button
    $('#btn-show-all-children').on('click', function(){
        // Enumerate all rows
        table.rows().every(function(){
            // If row has details collapsed
            if(!this.child.isShown()){
                // Open this row
                this.child(format(this.data())).show();
                $(this.node()).addClass('shown');
            }
        });
    });

    // Handle click on "Collapse All" button
    $('#btn-hide-all-children').on('click', function(){
        // Enumerate all rows
        table.rows().every(function(){
            // If row has details expanded
            if(this.child.isShown()){
                // Collapse row details
                this.child.hide();
                $(this.node()).removeClass('shown');
            }
        });
    });
});
