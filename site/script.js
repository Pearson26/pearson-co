const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#site-nav');
const tracking = window.PEARSON_TRACKING || {};
const consentKey = 'pearson_tracking_consent';

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

document.querySelectorAll('#year').forEach((year) => {
  year.textContent = new Date().getFullYear();
});

function loadScript(src) {
  const script = document.createElement('script');
  script.async = true;
  script.src = src;
  document.head.appendChild(script);
}

function enableTracking() {
  if (tracking.ga4MeasurementId && !window.gtag) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('consent', 'default', {
      analytics_storage: 'granted',
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted'
    });
    window.gtag('config', tracking.ga4MeasurementId);
    loadScript(`https://www.googletagmanager.com/gtag/js?id=${tracking.ga4MeasurementId}`);
  }

  if (tracking.metaPixelId && !window.fbq) {
    window.fbq = function fbq() { window.fbq.callMethod ? window.fbq.callMethod.apply(window.fbq, arguments) : window.fbq.queue.push(arguments); };
    window.fbq.queue = [];
    window.fbq.loaded = true;
    window.fbq.version = '2.0';
    window.fbq('init', tracking.metaPixelId);
    window.fbq('track', 'PageView');
    loadScript('https://connect.facebook.net/en_US/fbevents.js');
  }

  if (tracking.linkedInPartnerId && !window.lintrk) {
    window._linkedin_partner_id = tracking.linkedInPartnerId;
    window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
    window._linkedin_data_partner_ids.push(tracking.linkedInPartnerId);
    window.lintrk = function lintrk() { window.lintrk.q.push(arguments); };
    window.lintrk.q = [];
    loadScript('https://snap.licdn.com/li.lms-analytics/insight.min.js');
  }
}

function trackEvent(name, parameters = {}) {
  if (window.gtag) window.gtag('event', name, parameters);
  if (window.fbq && name === 'generate_lead') window.fbq('track', 'Lead');
  if (window.lintrk && name === 'generate_lead' && tracking.linkedInLeadConversionId) {
    window.lintrk('track', { conversion_id: tracking.linkedInLeadConversionId });
  }
}

document.querySelectorAll('[data-track]').forEach((element) => {
  element.addEventListener('click', () => trackEvent(element.dataset.track, {
    link_url: element.href || '',
    link_text: element.textContent.trim()
  }));
});

const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', () => {
    const button = form.querySelector('button[type="submit"]');
    trackEvent('lead_form_submit', { service: form.elements.service?.value || '' });
    button.textContent = 'Sending your enquiry…';
    button.disabled = true;
  });
}

const cookieBanner = document.querySelector('#cookie-banner');
const storedConsent = localStorage.getItem(consentKey);

if (storedConsent === 'accepted') enableTracking();
if (!storedConsent && cookieBanner) cookieBanner.hidden = false;

document.querySelector('#cookie-accept')?.addEventListener('click', () => {
  localStorage.setItem(consentKey, 'accepted');
  cookieBanner.hidden = true;
  enableTracking();
  trackEvent('consent_accepted');
});

document.querySelector('#cookie-reject')?.addEventListener('click', () => {
  localStorage.setItem(consentKey, 'essential');
  cookieBanner.hidden = true;
});

if (document.body.dataset.page === 'thanks') {
  trackEvent('generate_lead');
}
