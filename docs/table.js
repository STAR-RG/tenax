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
        'ajax': 'data.json', 
        'columns': [                
				{
            'targets': 0,
            'data': 'name',
            'checkboxes': {
               'selectRow': true,
             }
         	},
            {
                'className':      'details-control',
                'orderable':      false,
                'data':           null,
                'defaultContent': ''
            },
            { 'data': 'name' },
            { 'data': 'institution' },
            { 'data': 'bolsa-cnpq' },
            { 'data': 'area' },
            { 'data': 'num-tier-one' },
            { 'data': 'num-tier-two' },
            { 'data': 'num-tier-three' },
            { 'data': 'num-csindexbr-papers' },
            { 'data': 'num-csindexbr-journals' },
            { 'data': 'num-csindexbr-confs' }
        ],
        'select': {
         'style': 'multi'
      	},
        'order': [[6, 'desc']],
        'pageLength': 25
    });	
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function(){
        var tr = $(this).closest('tr');
        var row = table.row(tr);

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
   
   $('#btn-show-all').on('click', function(){
   	$.fn.dataTable.ext.search.pop();
   	table.search('').draw();
   });    
	       
   $('#btn-show-selected').on('click', function(){
   	$.fn.dataTable.ext.search.pop();
      $.fn.dataTable.ext.search.push(function (settings, data, dataIndex){             
      	return ($(table.row(dataIndex).node()).hasClass('selected')) ? true : false;
      });
      table.draw();	
   });
   	    
});
