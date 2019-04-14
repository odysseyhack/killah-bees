<%include file="/header.mako" />

<div class="col-md mt-4">
	<h1 class="mt-3">All dataset</h1>

	<table class="table mt-3">
		<thead>
			<tr>
				<th scope="col">Name</th>
				<th scope="col"></th>
			</tr>
		</thead>
		<tbody>
			% for file in fields['datasets']:
			<tr>
				<td>${file['name']}</td>
				<td><a href="/detector/${file['id']}" class="btn btn-info btn-sm">Check for breaches</a></td>
			</tr>
			% endfor
		</tbody>
	</table>
</div>


<%include file="/footer.mako" />