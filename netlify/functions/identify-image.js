const https = require('https');

/**
 * Netlify serverless function to identify a product from an uploaded image
 * using Google Gemini 1.5 Flash Vision API (if GEMINI_API_KEY is configured),
 * or returns a fallback indicator so client-side OCR / heuristics take over.
 */
exports.handler = async function (event, context) {
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'ERROR', message: 'Method Not Allowed' })
        };
    }

    let imagePayload = null;
    let userHint = '';
    try {
        const body = JSON.parse(event.body || '{}');
        imagePayload = body.image || body.image_data || body.imageData;
        userHint = (body.hint || body.query || '').trim();
    } catch (e) {
        return {
            statusCode: 400,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'ERROR', message: 'Invalid JSON request body' })
        };
    }

    if (!imagePayload) {
        return {
            statusCode: 400,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'ERROR', message: 'No image data provided' })
        };
    }

    // Extract base64 and mime type
    let mimeType = 'image/jpeg';
    let base64Data = imagePayload;
    if (imagePayload.startsWith('data:')) {
        const matches = imagePayload.match(/^data:([a-zA-Z0-9]+\/[a-zA-Z0-9-.+]+);base64,(.+)$/);
        if (matches) {
            mimeType = matches[1];
            base64Data = matches[2];
        }
    }

    const geminiApiKey = process.env.GEMINI_API_KEY;

    if (!geminiApiKey) {
        // No server-side API key configured; notify client to use client-side OCR
        return {
            statusCode: 200,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: 'FALLBACK',
                message: 'GEMINI_API_KEY not configured. Falling back to in-browser OCR / visual extraction.'
            })
        };
    }

    try {
        const promptText = `You are an expert e-commerce visual shopping assistant.
Examine this product photo or packaging image carefully.
Identify the exact product being shown.
${userHint ? `User provided extra hint: "${userHint}"` : ''}

Return ONLY a raw valid JSON object without markdown code blocks, backticks, or extra explanation with these exact keys:
{
  "product_name": "clean brand name followed by exact model and variant/shade, e.g. 'MARS Edge of Desire Lip Liner - 14 Choco Butter' or 'Apple iPhone 16 128GB Black'",
  "brand": "detected brand name, e.g. 'MARS', 'Apple', 'Samsung'",
  "category": "Beauty & Personal Care | Electronics | Fashion | General",
  "key_features": ["feature 1", "feature 2"],
  "estimated_price": 69
}`;

        const requestBody = JSON.stringify({
            contents: [
                {
                    parts: [
                        { text: promptText },
                        {
                            inline_data: {
                                mime_type: mimeType,
                                data: base64Data
                            }
                        }
                    ]
                }
            ],
            generationConfig: {
                temperature: 0.1,
                maxOutputTokens: 350
            }
        });

        const geminiResult = await new Promise((resolve, reject) => {
            const req = https.request(
                `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${geminiApiKey}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Content-Length': Buffer.byteLength(requestBody)
                    },
                    timeout: 10000
                },
                (res) => {
                    let data = '';
                    res.on('data', chunk => { data += chunk; });
                    res.on('end', () => {
                        try {
                            const parsed = JSON.parse(data);
                            resolve({ statusCode: res.statusCode, body: parsed });
                        } catch (err) {
                            reject(new Error('Invalid response from Gemini API'));
                        }
                    });
                }
            );

            req.on('error', reject);
            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Gemini API request timed out'));
            });

            req.write(requestBody);
            req.end();
        });

        if (geminiResult.statusCode === 200 && geminiResult.body?.candidates?.[0]?.content?.parts?.[0]?.text) {
            let rawText = geminiResult.body.candidates[0].content.parts[0].text.trim();
            // Strip markdown fences if present
            rawText = rawText.replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/```$/i, '').trim();
            const productData = JSON.parse(rawText);

            return {
                statusCode: 200,
                headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    status: 'SUCCESS',
                    source: 'GEMINI_VISION',
                    product_name: productData.product_name,
                    brand: productData.brand,
                    category: productData.category,
                    key_features: productData.key_features || [],
                    estimated_price: productData.estimated_price || null
                })
            };
        } else {
            console.warn('Gemini response error:', geminiResult.body);
            return {
                statusCode: 200,
                headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    status: 'FALLBACK',
                    message: 'Gemini visual recognition was inconclusive. Falling back to OCR.'
                })
            };
        }

    } catch (err) {
        console.warn('Gemini vision error:', err.message);
        return {
            statusCode: 200,
            headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: 'FALLBACK',
                message: err.message
            })
        };
    }
};
