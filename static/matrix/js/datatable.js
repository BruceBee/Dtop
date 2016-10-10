$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
    return {
        "iStart":         oSettings._iDisplayStart,
        "iEnd":           oSettings.fnDisplayEnd(),
        "iLength":        oSettings._iDisplayLength,
        "iTotal":         oSettings.fnRecordsTotal(),
        "iFilteredTotal": oSettings.fnRecordsDisplay(),
        "iPage":          oSettings._iDisplayLength === -1 ?
            0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
        "iTotalPages":    oSettings._iDisplayLength === -1 ?
            0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
    };
}
 
/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
    "bootstrap": {
        "fnInit": function( oSettings, nPaging, fnDraw ) {
            var oLang = oSettings.oLanguage.oPaginate;
            var fnClickHandler = function ( e ) {
                e.preventDefault();
                if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
                    fnDraw( oSettings );
                }
            };
 
            $(nPaging).addClass('pagination').append(
                '<ul>'+
		    '<li class="first disabled"><a href="#">'+oLang.sFirst+'</a></li>'+ //此处添加
                    //'<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+ //带箭头
                    '<li class="prev disabled"><a href="#">'+oLang.sPrevious+'</a></li>'+
                    //'<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
                    '<li class="next disabled"><a href="#">'+oLang.sNext+'</a></li>'+
		    '<li class="last disabled"><a href="#">'+oLang.sLast+'</a></li>'+//此处添加
                '</ul>'
            );
            var els = $('a', nPaging);
	    $(els[0]).bind( 'click.DT', { action: "first" }, fnClickHandler );//此处添加
            $(els[1]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
            $(els[2]).bind( 'click.DT', { action: "next" }, fnClickHandler );
	    $(els[3]).bind( 'click.DT', { action: "last" }, fnClickHandler );//此处添加
        },
 
        "fnUpdate": function ( oSettings, fnDraw ) {
            var iListLength = 5;
            var oPaging = oSettings.oInstance.fnPagingInfo();
            var an = oSettings.aanFeatures.p;
            var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);
 
            if ( oPaging.iTotalPages < iListLength) {
                iStart = 1;
                iEnd = oPaging.iTotalPages;
            }
            else if ( oPaging.iPage <= iHalf ) {
                iStart = 1;
                iEnd = iListLength;
            } else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
                iStart = oPaging.iTotalPages - iListLength + 1;
                iEnd = oPaging.iTotalPages;
            } else {
                iStart = oPaging.iPage - iHalf + 1;
                iEnd = iStart + iListLength - 1;
            }
 
            for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
                // Remove the middle elements
                //$('li:gt(0)', an[i]).filter(':not(:last)').remove();
 		$('li:gt(1)', an[i]).filter(':lt(-2)').remove();//此处修改 $('li:gt(0)', an[i]).filter(':not(:last)').remove();

                // Add the new list items and their event handlers
                for ( j=iStart ; j<=iEnd ; j++ ) {
                    sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
                    $('<li '+sClass+'><a href="#">'+j+'</a></li>')
                        //.insertBefore( $('li:last', an[i])[0] )
			  .insertBefore( $('li:eq(-2)', an[i])[0] )//此处修改 .insertBefore( $('li:last', an[i])[0] )
                        .bind('click', function (e) {
                            e.preventDefault();
                            oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
                            fnDraw( oSettings );
                        } );
                }
 
                // Add / remove disabled classes from the static elements
                if ( oPaging.iPage === 0 ) {
                    //$('li:first', an[i]).addClass('disabled');
		      $('li:lt(2)', an[i]).addClass('disabled'); //此处修改 $('li:first', an[i]).addClass('disabled');
                } else {
                    //$('li:first', an[i]).removeClass('disabled');
		      $('li:lt(2)', an[i]).removeClass('disabled'); //此处修改$('li:first', an[i]).removeClass('disabled');
                }
 
                if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
                    //$('li:last', an[i]).addClass('disabled');
			$('li:gt(-3)', an[i]).addClass('disabled'); //此处修改$('li:last', an[i]).addClass('disabled');
                } else {
                    //$('li:last', an[i]).removeClass('disabled');
			 $('li:gt(-3)', an[i]).removeClass('disabled'); //此处修改$('li:last', an[i]).removeClass('disabled');
                }
            }
        }
    }
} );
