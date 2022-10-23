#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform sampler2D u_texture;
uniform sampler2D n_texture;
uniform sampler2D r_texture;
uniform float metallic = 0.0;

uniform Light light;
uniform vec3 camPos;
uniform float Pi = 3.14159265359;
uniform float ZeroAvoid = 0.0000001;

//normal distribution function
float distributionGGX(float NdotH, float roughness)
{
    float a = roughness * roughness;
    float a2 = a * a;
    float denom = (NdotH * NdotH) * (a2 - 1.0) + 1.0;
    denom = denom * denom * Pi;
    return a2/max(denom,0.0000001); //prevent divide by zero
}

float geometrySmith(float NdotV, float NdotL, float roughness)
{
    float r = roughness + 1.0;
    float k = (r * r) / 8.0;
    float ggx1 = NdotV / (NdotV * (1.0 - k) + k);
    float ggx2 = NdotL / (NdotL * (1.0 - k) + k);
    return ggx1 * ggx2;
}

vec3 fresnelSchlick(float HdotV, vec3 baseReflectivity)
{
    return baseReflectivity + (1.0 - baseReflectivity) * pow(1.0 - HdotV, 5.0);
}

//basic phong lighting
//------
// vec3 getLight(vec3 color, vec3 nColor)
// {
//     vec3 Normal = normalize(normal+(nColor*2.0f - 1.0f));

//     //ambient light
//     vec3 ambient = light.Ia;

//     //diffuse light
//     vec3 lightDir = normalize(light.position - fragPos);
//     float diff = max(0,dot(lightDir,Normal));
//     vec3 diffuse = diff * light.Id;

//     //specular light
//     vec3 viewDir = normalize(camPos-fragPos);
//     vec3 reflectDir = reflect(-lightDir,Normal);
//     float spec = pow(max(dot(viewDir,reflectDir),0),32);
//     vec3 specular = spec * light.Is;

//     return color * (ambient + diffuse + specular);
// }

void main ()
{
    float gamma = 2.2;
    float roughness = texture(r_texture,uv_0).r;
    vec3 nColor = texture(n_texture,uv_0).rgb;
    vec3 N = normalize(normal+(texture(n_texture,uv_0).rgb*2.0-1.0));
    vec3 V = normalize(camPos-fragPos);

    vec3 baseReflectivity = mix(vec3(0.04),texture(u_texture,uv_0).rgb,metallic); // lerp between albedo, metallic

    vec3 dirLighting = vec3(0.0);
    for(int i = 0; i<1; ++i)
    {
        vec3 L = normalize(light.position-fragPos);
        vec3 H = normalize(V + L);
        float distance = length(light.position - fragPos);
        float attenuation = 1.0/(distance*distance);
        vec3 radiance = light.Id * attenuation;

        float NdotV = max(dot(N,V),0.0000001);
        float NdotL = max(dot(N,L),0.0000001);
        float HdotV = max(dot(H,V),0.0);
        float NdotH = max(dot(N,H),0.0);

        float D = distributionGGX(NdotH,roughness);
        float G = geometrySmith(NdotV,NdotL,roughness);
        vec3 F = fresnelSchlick(HdotV,baseReflectivity);

        vec3 specularBRDF = D * G * F;
        specularBRDF /= max(ZeroAvoid,(4.0 * NdotV * NdotL));

        vec3 kD = mix(vec3(1.0) - F,vec3(0.0),metallic);
        vec3 diffuseBRDF = kD * texture(u_texture,uv_0).rgb;
        dirLighting += (diffuseBRDF + specularBRDF) * radiance * NdotL;
    }

    vec3 ambient = light.Ia * texture(u_texture,uv_0).rgb;

    vec3 lightDir = normalize(light.position - fragPos);
    vec3 reflectDir = reflect(-lightDir,N);
    float spec = pow(max(dot(V,reflectDir),ZeroAvoid),metallic);
    vec3 specular = spec * light.Is;

    vec3 color = ambient + dirLighting + specular;
    //base gamma adjust. if gamma is fixed, base color will be more brighter.
    //should be enabled when using phong/blinn.
    //should be disabled when using ue shading.
    //--------
    // color = color / (color + vec3(1.0));
    // color = pow(color,1/vec3(gamma));
    fragColor = vec4(color, 1.0);

}