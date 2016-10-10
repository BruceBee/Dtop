(function ($) {

   $.fn.pickList = function (options) {

      var opts = $.extend({}, $.fn.pickList.defaults, options);

      this.fill = function () {
         var option = '';

         $.each(opts.data, function (key, val) {
            option += '<option id=' + val.id + '>' + val.text + '</option>';
         });
         this.find('#pickData').append(option);
      };
      this.controll = function () {
         var pickThis = this;

         $("#pAdd").on('click', function () {
            var p = pickThis.find("#pickData option:selected");
            p.clone().appendTo("#pickListResult");
            p.remove();
         });

         $("#pAddAll").on('click', function () {
            var p = pickThis.find("#pickData option");
            p.clone().appendTo("#pickListResult");
            p.remove();
         });

         $("#pRemove").on('click', function () {
            var p = pickThis.find("#pickListResult option:selected");
            p.clone().appendTo("#pickData");
            p.remove();
         });

         $("#pRemoveAll").on('click', function () {
            var p = pickThis.find("#pickListResult option");
            p.clone().appendTo("#pickData");
            p.remove();
         });
      };
      this.getValues = function () {
         var objResult = [];
         this.find("#pickListResult option").each(function () {
            objResult.push({id: this.id, text: this.text});
         });
         return objResult;
      };
      this.init = function () {
         var pickListHtml =
                 "<div class='row'>" +
                 "  <div class='col-sm-5'>" +
                 "	 <select class='form-control pickListSelect' id='pickData' multiple></select>" +
                 " </div>" +
                 " <div class='col-sm-2 pickListButtons'>" +
                 "	<button id='pAdd' class='btn btn-primary btn-sm'>" + opts.add + "</button>" +
                 "      <button id='pAddAll' class='btn btn-primary btn-sm'>" + opts.addAll + "</button>" +
                 "	<button id='pRemove' class='btn btn-primary btn-sm'>" + opts.remove + "</button>" +
                 "	<button id='pRemoveAll' class='btn btn-primary btn-sm'>" + opts.removeAll + "</button>" +
                 " </div>" +
                 " <div class='col-sm-5'>" +
                 "    <select class='form-control pickListSelect' id='pickListResult' multiple></select>" +
                 " </div>" +
                 "</div>";

         this.append(pickListHtml);

         this.fill();
         this.controll();
      };

      this.init();
      return this;
   };

   $.fn.pickList.defaults = {
      add: 'Add',
      addAll: 'Add All',
      remove: 'Remove',
      removeAll: 'Remove All'
   };


}(jQuery));


