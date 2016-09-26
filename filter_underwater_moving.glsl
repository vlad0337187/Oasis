/* Для работы на вызывающем объекте должно быть установлено свойство с именем timer типа Timer.
*/

uniform sampler2D bgl_RenderedTexture;
uniform float timer;

vec2 texcoord = vec2(gl_TexCoord[0]).st;
vec2 cancoord = vec2(gl_TexCoord[3]).st;

void main(void)
{
    texcoord.y = texcoord.y + (sin(cancoord.x*4.0+timer*10)*0.001); // 4.0+timer*3.5)*0.005); и там и там
    texcoord.x = texcoord.x + (cos(cancoord.y*4.0+timer*3.5)*0.005);


	gl_FragColor = texture2D(bgl_RenderedTexture, texcoord);
	
}