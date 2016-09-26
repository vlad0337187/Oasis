// Modernized shader by
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

//uniform float avgL;

const float dens = 0.8; // Density
const float dec = 0.98; // Decay
//const float weight = 0.2;
uniform float weight;
float exp = 0.05; // Exposure

// Light Screen (Origin if effect is not working Play with X & Y)

uniform float x; // 0.0 - 1.0
uniform float y; // 0.0 - 1.0

uniform vec2 lightScreenPos;

// Number of Ray Samples (Quality 1 - 128)

const int raySamples = 33;

void main()
{

    vec4 origin = vec4(0);
    vec4 sample = vec4(0);
    vec4 mask = vec4(0);

    vec2 lightScreenPos = vec2(x,y);

    vec2 deltaTexCoord = vec2(gl_TexCoord[0]) - lightScreenPos;
	vec2 texCoo = gl_TexCoord[0].st;
	deltaTexCoord *= 1.0 / float(raySamples) * dens;
	float illumDecay = 1.0;

   for(int i=0; i < raySamples ; i++)
   {
       texCoo -= deltaTexCoord;

        if (texture2D(bgl_DepthTexture, texCoo).r > 0.9989)
        {
            sample += texture2D(bgl_RenderedTexture, texCoo);
        }
        
        sample *= illumDecay * weight;
    
        origin += sample;
        illumDecay *= dec;
    }
    
    vec2 texcoord = vec2(gl_TexCoord[0]);
 
    gl_FragColor = texture2D(bgl_RenderedTexture, texcoord) + (origin*exp);

}

