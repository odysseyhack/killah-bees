<%include file="/header.mako" />

<div class="col-md mt-4">
	% if breach:
	<div class="jumbotron text-light bg-danger mt-4">
		<h1 class="display-4">Privacy breach detected.</h1>
		<p class="lead">Don't publish the selected fields.</p>
	</div>
	% else:
	<div class="jumbotron text-light bg-success mt-4">
		<h1 class="display-4">All safe, no breaches detected.</h1>
		<p class="lead">You can publish the selected fields of this dataset.</p>
	</div>
	% endif
</div>

<%include file="/footer.mako" />