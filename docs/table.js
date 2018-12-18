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
               /*'selectCallback': function(nodes, selected){
                  // If "Show all" is not selected
                  if($('#ctrl-show-selected').val() !== 'all'){
                     // Redraw table to include/exclude selected row
                     table.draw(false);                  
                  }            
               }*/
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
        'select': 'multi',
        'order': [[6, 'desc']],
        'pageLength': 20
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
       
   $('#example thead').on('click', 'input:checkbox', function () {
		if($(this).is(':checked')){    		
    		$(this).prop('checked', true);
    		$('input.dt-checkboxes').each(function () {
    			$(this).prop('checked', true);
         	var tr = $(this).closest('tr');
         	$(tr).addClass('check-selected');
		 	});         
		} else {
			$(this).prop('checked', false);
    		$('input.dt-checkboxes').each(function () {
    			$(this).prop('checked', false);
         	var tr = $(this).closest('tr');
         	$(tr).removeClass('check-selected');
		 	});             		
    	}
	});
	
	$('#example tbody').on( 'click', 'input.dt-checkboxes', function () {
    	var tr = $(this).closest('tr');
   	if ($(tr).hasClass('check-selected')) {
        $(tr).removeClass('check-selected');
    	} else {
        $(tr).addClass('check-selected');
    	}
	});	
	
	// Handle click on "Show All" button
    $('#btn-show-all').on('click', function(){
       $('input.dt-checkboxes').each(function () {
         	$(this).prop('checked', false);
         	var tr = $(this).closest('tr');
         	$(tr).removeClass('check-selected');
		 });
		 $('#example thead input:checkbox').prop('checked', false);  
       $.fn.dataTable.ext.search.pop();
       table.draw();
    });	
    
    // Handle click on "Show selected" button
	$('#btn-show-selected').on('click', function(){
       $.fn.dataTable.ext.search.pop();
       $.fn.dataTable.ext.search.push(function(settings, data, dataIndex){
               return ($(table.row(dataIndex).node()).hasClass('check-selected')) ? true : false;
       });
       table.draw();
    });
   
});
