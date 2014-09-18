(function($){
	function url_to(url) {
		location.href=url;	
	}

	$('[name="select_all"]').click(function(){
		$('[name="select_id"]:not(:checked)').click();
	});
	$('[name="select_none"]').click(function(){
		$('[name="select_id"]:checked').click();
	});
	$('[name="select_invert"]').click(function(){
		$('[name="select_id"]').click();		
	});
	$('[name="select_delete"]').click(function(){
		var list_id = new Array();	
		if ($('[name="select_id"]:checked').length>0) {
			allow = confirm('你确定要删除所有选中项');
			if (allow) {
				$('[name="select_id"]:checked').each(function(i){
					list_id[i] = $(this).val();	
				});
				url_to(location.pathname+'/delete/'+list_id.join());
			}
		} else {
			alert('请至少选中一项');		
		}
	})
})(jQuery);
