// Версия: 1
uniform sampler2D bgl_RenderedTexture;
vec2 texCoord = gl_TexCoord[0].st;
uniform float sun_x;
uniform float sun_y;

void main() {
       vec3 color = texture2D(bgl_RenderedTexture,texCoord).rgb;
       // from 1 - near, to -1 - far
       float nearness = 1 - (abs(sun_x) + abs(sun_y));
       float coefficient = nearness / 30;
       //color.b = color.b / 4;
       //color.g = color.g / 4;
       //if (nearness <= 0.5) {
           color.r = color.r + coefficient;
           color.g = color.g + (coefficient / 1.5);
           color.b = color.b - (coefficient);
       //}
       gl_FragColor = vec4(color,1.0); 
}