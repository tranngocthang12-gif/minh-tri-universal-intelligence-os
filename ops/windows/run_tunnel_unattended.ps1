$ErrorActionPreference = 'Stop'

$runtime = $PSScriptRoot
$python = Join-Path $runtime '.venv\Scripts\python.exe'
$exe = Join-Path $runtime 'tunnel-client\v0.0.15\tunnel-client.exe'
$healthFile = Join-Path $runtime 'tunnel-client\minhtri-health.url'
$sealed = Join-Path $env:LOCALAPPDATA 'MINH_TRI\tunnel.runtime.dpapi'

foreach ($path in @($python, $exe, $sealed)) { if (!(Test-Path $path)) { throw "BLOCKED_REQUIRED_RUNTIME_INPUT_MISSING: $path" } }
$enc = (Get-Content -Raw $sealed).Trim()
if ([string]::IsNullOrWhiteSpace($enc)) { throw 'BLOCKED_EMPTY_DPAPI_SECRET' }
$sec = ConvertTo-SecureString $enc
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try {
    $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    if ([string]::IsNullOrWhiteSpace($plain)) { throw 'BLOCKED_DPAPI_UNSEAL_EMPTY' }
    $env:CONTROL_PLANE_API_KEY = $plain
    $env:PYTHONPATH = $runtime
    & $python -m minhtri.runtime_supervisor -- $exe run --profile minh-tri-local-brain --health.listen-addr 127.0.0.1:0 --health.url-file $healthFile
    exit $LASTEXITCODE
} finally {
    Remove-Item Env:CONTROL_PLANE_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    if ($bstr -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
    $plain = $null
}
