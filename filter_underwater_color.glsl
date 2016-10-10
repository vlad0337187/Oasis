// Revision: 1
// Author: Vladislav Naumov. naumovvladislav@list.ru; github.com/vlad1777d; vk.com/naumovvladislav
// License: CC-BY. To use this under other license contact author.

uniform sampler2D bgl_RenderedTexture;
vec2 texCoord = gl_TexCoord[0].st;

void main() {
       vec3 color = texture2D(bgl_RenderedTexture,texCoord).rgb;
       color.b = color.b / 4;
       color.g = color.g / 4;
       color.r = color.r / 5;
       gl_FragColor = vec4(color,1.0); 
}