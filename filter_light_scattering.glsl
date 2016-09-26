// This is original shader by Martin Upitiz
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

// This values must be in object's properties, they must be in float format
uniform float exposure;  // (default = 0.150)
uniform float decay;  // (default = 0.980)
uniform float density;  // (default = 0.900)
uniform float weight;  // (default = 0.350)

uniform float x;  // (default = 0)
uniform float y;  // (default = 0)

uniform vec2 lightPositionOnScreen;


const int NUM_SAMPLES = 50;

void main()
{

    vec4 light = vec4(0);
    vec4 sample = vec4(0);
    vec4 mask = vec4(0);

    vec2 lightPositionOnScreen = vec2(x*0.82,y*0.925);

    vec2 deltaTexCoord = vec2(gl_TexCoord[0]) - lightPositionOnScreen;
	vec2 texCoo = gl_TexCoord[0].st;
	deltaTexCoord *= 1.0 / float(NUM_SAMPLES) * density;
	float illuminationDecay = 1.0;

//doing light-rays    

   for(int i=0; i < NUM_SAMPLES ; i++)
   {
   texCoo -= deltaTexCoord;
     
//comapring depths to render only sky and sun.
//This should be before blurring, but cannot figure out how..

if (texture2D(bgl_DepthTexture, texCoo).r > 0.9989)
{
    sample += texture2D(bgl_RenderedTexture, texCoo);
}

    
    sample *= illuminationDecay * weight;

    light += sample;
    illuminationDecay *= decay;
    }
    vec2 texcoord = vec2(gl_TexCoord[0]);
 
gl_FragColor = texture2D(bgl_RenderedTexture, texcoord) + (light*exposure);

}




   