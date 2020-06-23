<template>
	<div>
		<h1>404 - not found</h1>
		<router-link to="/">
			<span class="homepage-url">Back to homepage >></span>
		</router-link>
	</div>
</template>


<style>
	h1 {
		padding-top: 6.25rem;
		font-size: 3.125rem;
		display: block;
		font-weight: bold;
		color: #29323C;
	}
	
	.homepage-url {
		font-size: 1.25rem;
		display: block;
		color: #29323C;
		cursor: pointer;
	}
	
	.homepage-url:hover {
		text-decoration: underline;
		color: cadetblue;
	}
</style>
