/*Сделал Martin Upitis.
Для работы нужны на объекте, к которому прикреплен кирпичик с этим 2D фильтром, свойства timer (типа timer) (значение по-умолчанию: 0.0) и noise_amount (типа float) (значение по-умолчанию: 0.1).

*/

uniform sampler2D bgl_RenderedTexture;

uniform float timer;
uniform float noise_amount;

void main(void)
{ 	
	float noiseR =  (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer)) * 43758.5453));
	float noiseG =  (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer*2.0)) * 43758.5453)); 
	float noiseB =  (fract(sin(dot(gl_TexCoord[0].st ,vec2(12.9898,78.233)+timer*3.0)) * 43758.5453));
	
	vec4 noise = vec4(noiseR,noiseG,noiseB,1.0);
	   
	gl_FragColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st) + (noise*noise_amount);
}