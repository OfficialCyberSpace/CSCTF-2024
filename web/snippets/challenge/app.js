const express = require('express');
const puppeteer = require('puppeteer');
const crypto = require('node:crypto');
const path = require('node:path');
const fs = require('node:fs');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const fillTemplate = require('es6-dynamic-template');

const app = express();
const port = 3000;

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);
const translate = text => {
	return text.replace( /J/gi, 'Ｊ' )
		.replace( /A/gi, 'Α' )
		.replace( /B/gi, 'Β' )
		.replace( /D/gi, 'Ⅾ' )
		.replace( /K/gi, 'К' )
		.replace( /H/gi, 'Ｈ' )
		.replace( /M/gi, 'М' )
		.replace( /O/gi, '0' )
		.replace( /\$/gi, '＄' ) 
		.replace( /%/gi, '％' ) 
		.replace( /\//gi, '╱' )
		.replace( /\\/gi, '＼' )
		.replace( /\{/gi, '｛' )
		.replace( /\}/gi, '｝' )
		.replace( /@/gi, '＠' )
		.replace( /\[/gi, '［' )
		.replace( /\]/gi, '］' )
		.replace( /\^/gi, '＾' )
		.replace( /_/gi, '＿' )
}
DOMPurify.addHook( 'beforeSanitizeElements', node => {
	if ( node.nodeName && node.nodeName === '#text' ) {
		node.textContent = translate( node.textContent );
	}
} );
DOMPurify.addHook( 'uponSanitizeAttribute', (node, event) => {
	event.attrValue = translate( event.attrValue );
} );

app.use(express.urlencoded({ extended: false }));

app.use(express.static('static'));


app.get('/', async (req, res) => {
	if ( !req.query.name || !req.query.snippet ) {
		return res.redirect( "/home.htm" );
	}

	const name = req.query.name;
	const snippet = DOMPurify.sanitize( req.query.snippet );
	const nonce = crypto.randomBytes( 16 ).toString('hex');
	const script = 	`
		document.addEventListener( 'DOMContentLoaded', function () {
			document.getElementById( 'viewButton' ).addEventListener(
				'click',
				function () {
					document.getElementById( 'viewSnippet' ).innerHTML = snippet;
					document.getElementById( 'viewSnippet' ).id = 'snippetDisplay';
				}
			);
		} );
		var snippet = ${JSON.stringify(snippet)};
		// @license http://unlicense.org/UNLICENSE Unlicense`;

	const html = fillTemplate(
		fs.readFileSync( 'static/view.htm', 'utf-8' ),
		{ nonce, script, name, snippet }
	);
	
	return res.
		set( {
			'Content-Security-Policy': `script-src 'nonce-${nonce}'`
		} ).send( html );
} );

app.post( '/report', async (req, res) => {
	try {

		if ( !req.body.url || !req.body.url.match( /^https:\/\/snippets-web-challs.csc.tf\// ) ) {
			throw new Error( "Invalid url" );
		}
		const url = req.body.url;
		browser = await puppeteer.launch({
			headless: true,
			args: [
				'--incognito',
				"--no-sandbox",
				"--disable-setuid-sandbox",
				"--js-flags=--noexpose_wasm,--jitless",
			]
		});

		context = await browser.createBrowserContext();
		page = await context.newPage();
		page.setCookie( { name: 'flag', value: process.env.FLAG, domain: 'snippets-web-challs.csc.tf' } );
		page.setDefaultTimeout( 2000 );

		await page.goto( url, {timeout: 2000, waitUntil: 'domcontentloaded' } );
		await new Promise( (r) => setTimeout(r, 200 ) );
		await page.click( '#viewButton' );
		await new Promise( (r) => setTimeout(r, 2000 ) );
		await browser.close();
	} catch ( e ) {
		return res.status(500).set( 'content-type', 'text/plain' ).send( "Error: " + e.message );
	}
	return res.send( '<link rel="stylesheet" href="/style.css"><body><main>Thank you for the report. Our admin will check out the URL shortly' );
} );

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
