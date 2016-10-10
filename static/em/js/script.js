$(document).scroll(function(){
							
	var baseheight=$(document).scrollTop();
	
	if(baseheight>500&&$(".list_head1").position().top-baseheight>0&&$(".list_head2").position().top-baseheight>0){
		$(".list_head").addClass("list-header-fixed");
		$(".list_head1").removeClass("list-header-fixed");	
		$(".list_head2").removeClass("list-header-fixed");	
	}
		
	if(baseheight<500){
		$(".list_head").removeClass("list-header-fixed");	
		$(".list_head1").removeClass("list-header-fixed");
		$(".list_head2").removeClass("list-header-fixed");	
	}
			
	if(baseheight>500&&$(".list_head1").position().top-baseheight<0&&$(".list_head2").position().top-baseheight>0){
		$(".list_head1").addClass("list-header-fixed");
		$(".list_head").removeClass("list-header-fixed");	
		$(".list_head2").removeClass("list-header-fixed");	
	}
		
	if(baseheight>500&&$(".list_head1").position().top-baseheight>0&&$(".list_head2").position().top-baseheight<0){
		$(".list_head2").addClass("list-header-fixed");
		$(".list_head1").removeClass("list-header-fixed");	
		$(".list_head").removeClass("list-header-fixed");		
	}
	
})
